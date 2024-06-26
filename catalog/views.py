from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import DetailView, UpdateView, TemplateView, \
    CreateView, ListView, DeleteView
from catalog.models import Product, Contact, Blog


class ContactsListView(ListView):
    model = Contact
    template_name = 'contacts.html'


class ProductListView(ListView):
    model = Product
    paginate_by = 4


class ProductCreateView(CreateView):
    model = Product
    fields = ('product_name', 'description',
              'preview_image', 'category', 'price',)
    success_url = reverse_lazy('catalog:product_list')


class ProductDetailView(DetailView):
    model = Product


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'preview_image', 'is_published',)
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            blog = form.save()
            blog.slug = slugify(blog.title)
            blog.save()

        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'preview_image', 'is_published',)

    def get_success_url(self):
        return reverse('catalog:blog_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if form.is_valid():
            blog = form.save()
            blog.slug = slugify(blog.title)
            blog.save()

        return super().form_valid(form)


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')

