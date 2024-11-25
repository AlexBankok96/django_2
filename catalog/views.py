from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from catalog.forms import ProductForm, VersionForm, ModeratorForm
from catalog.models import Product, Version
from catalog.services import get_categories_from_cache

class ContactsPageView(TemplateView):
    template_name = "catalog/contacts.html"


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_categories_from_cache()
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    @method_decorator(cache_page(60))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        active_versions = product.versions.filter(version_flag=True)
        context['active_versions'] = active_versions
        context['categories'] = get_categories_from_cache()
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:catalog_list")

    def form_valid(self, form):
        cleaned_data = form.cleaned_data['name'].lower()
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in forbidden_words:
            if word in cleaned_data:
                form.add_error('name', 'Данное название не подходит.')
                return self.form_invalid(form)

        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product_formset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = product_formset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = product_formset(instance=self.object)
        context_data['categories'] = get_categories_from_cache()
        return context_data


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:catalog_list")

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product_formset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = product_formset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = product_formset(instance=self.object)
        context_data['categories'] = get_categories_from_cache()  # Добавляем категории в контекст
        return context_data


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:catalog_list')


class VersionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Version
    form_class = VersionForm
    permission_required = 'catalog.add_version'
    success_url = reverse_lazy('catalog:catalog_list')

    def form_valid(self, form):
        product = form.cleaned_data['product']
        if not self.request.user == product.owner and not self.request.user.has_perm('catalog.change_product'):
            form.add_error('product', 'У вас нет прав на создание версии для этого продукта.')
            return self.form_invalid(form)
        return super().form_valid(form)


class VersionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Version
    form_class = VersionForm
    permission_required = 'catalog.change_version'
    success_url = reverse_lazy('catalog:catalog_list')

    def form_valid(self, form):
        version = form.instance
        if not self.request.user == version.product.owner and not self.request.user.has_perm('catalog.change_product'):
            form.add_error('product', 'У вас нет прав на редактирование версии этого продукта.')
            return self.form_invalid(form)
        return super().form_valid(form)


class VersionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Version
    permission_required = 'catalog.delete_version'
    success_url = reverse_lazy('catalog:catalog_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        version = self.get_object()
        if self.request.user != version.product.owner and not self.request.user.has_perm('catalog.change_product'):
            return queryset.none()
        return queryset
