from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import DetailView, UpdateView, TemplateView, \
    CreateView, ListView, DeleteView
from catalog.forms import ProductForm, VersionForm, BlogForm
from catalog.models import Product, Contact, Blog, Version
from catalog.services import send_email


class ContactsListView(ListView):
    model = Contact
    template_name = 'contacts.html'


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        product = form.save()
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
        ProductFormset = inlineformset_factory(Product, Version, VersionForm,
                                               extra=1)
        if self.request.method == 'POST':
            context['formset'] = ProductFormset(self.request.POST,
                                                instance=self.object)
        else:
            context['formset'] = ProductFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
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
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset))


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')


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
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        if self.object.view_counter == 100:
            send_email(self.object)
        self.object.save()
        return self.object


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


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')
