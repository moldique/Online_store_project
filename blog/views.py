from django.urls import reverse_lazy
from django.db.models import F
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # На списке показываем только опубликованные
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Инкремент счётчика просмотров
        BlogPost.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        obj.refresh_from_db(fields=['views_count'])
        return obj


class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    permission_required = 'blog.can_manage_blog'
    login_url = '/users/login/'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для создания записей в блоге.')
        return redirect('blog:post_list')


class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BlogPost
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    permission_required = 'blog.can_manage_blog'
    login_url = '/users/login/'

    def get_success_url(self):
        # После редактирования переадресуем на страницу отредактированной записи
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для редактирования записей в блоге.')
        return redirect('blog:post_detail', pk=self.kwargs['pk'])


class BlogPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    permission_required = 'blog.can_manage_blog'
    login_url = '/users/login/'

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для удаления записей в блоге.')
        return redirect('blog:post_detail', pk=self.kwargs['pk'])

