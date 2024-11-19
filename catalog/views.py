from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version


# Создавайте свои мнения здесь.

class ContactsPageView(TemplateView):
    template_name = "catalog/contacts.html"


class ProductListView(LoginRequiredMixin, ListView):
    model = Product


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        active_versions = product.versions.filter(version_flag=True)
        context['active_versions'] = active_versions
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:catalog_list")

    def form_valid(self, form):
        cleaned_data = form.cleaned_data['name'].lower()
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']

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
        return context_data


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:catalog_list")

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
        return context_data


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:catalog_list')