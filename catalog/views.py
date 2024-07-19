from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import DetailView, UpdateView, CreateView, ListView, \
    DeleteView
from catalog.forms import ProductForm, VersionForm, BlogForm, \
    ProductModerationForm, BlogModerationForm
from catalog.models import Product, Contact, Blog, Version, Category
from catalog.services import send_email, cache_product_list_by_category, \
    cache_category_list


class ContactsListView(ListView):
    model = Contact
    template_name = 'contacts.html'


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        category_id = self.kwargs['pk']
        if self.request.user.is_superuser or self.request.user.has_perm('catalog.view_product'):
            return cache_product_list_by_category(category_id)
        return cache_product_list_by_category(category_id).filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_pk'] = self.kwargs['pk']
        for obj in context['object_list']:
            obj.active_version = obj.versions.filter(
                is_active=True).first() if obj.versions.filter(
                is_active=True).first() else "Активная версия не найдена"
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_pk'] = Product.objects.get(pk=self.kwargs['pk']).category.pk
        if type(context['form']) == ProductForm:
            ProductFormset = inlineformset_factory(Product, Version, VersionForm,
                                                   extra=1)
            if self.request.method == 'POST':
                context['formset'] = ProductFormset(self.request.POST,
                                                    instance=self.object)
            else:
                context['formset'] = ProductFormset(instance=self.object)
        return context

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return ProductForm
        if user.has_perms(
            ['catalog.product_set_published_status', 'catalog.product_change_description',
             'catalog.product_change_category']):
            return ProductModerationForm
        raise PermissionDenied

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context.get('formset')
        if formset:
            if form.is_valid() and formset.is_valid():
                active_version = 0
                for i in formset.forms:
                    if i.cleaned_data.get('is_active'):
                        active_version += 1
                    if active_version > 1:
                        form.add_error(None,
                                       'Вы можете выбрать только одну активную версию')
                        return self.form_invalid(form)
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        elif form.is_valid():
            form.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset))


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_pk'] = Product.objects.get(pk=self.kwargs['pk']).category.pk
        return context


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            blog = form.save()
            blog.author = self.request.user
            blog.slug = slugify(blog.title)
            blog.save()
        return super().form_valid(form)


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.has_perm('catalog.blog_set_published_status'):
            return super().get_queryset()
        return super().get_queryset().filter(is_published=True)


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.is_published:
            self.object.view_counter += 1
            if self.object.view_counter == 100:
                send_email(self.object)
            self.object.save()
            return self.object
        else:
            if self.request.user.has_perm('catalog.blog_set_published_status') or self.request.user.is_superuser:
                return self.object
            else:
                self.object = None


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm

    def get_success_url(self):
        return reverse('catalog:blog_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if form.is_valid():
            blog = form.save()
            blog.slug = slugify(blog.title)
            blog.save()

        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.author or user.is_superuser:
            return BlogForm
        if user.has_perms(['catalog.blog_set_published_status']):
            return BlogModerationForm
        raise PermissionDenied


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category

    def get_queryset(self, *args, **kwargs):
        return cache_category_list()
