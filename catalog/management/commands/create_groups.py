from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product
from blog.models import BlogPost


class Command(BaseCommand):
    help = 'Создает группы "Модератор продуктов" и "Контент-менеджер" с необходимыми правами'

    def handle(self, *args, **options):
        # Создаем группу "Модератор продуктов"
        group, created = Group.objects.get_or_create(name='Модератор продуктов')
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Группа "Модератор продуктов" создана')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Группа "Модератор продуктов" уже существует')
            )

        # Получаем контент-тип для модели Product
        content_type = ContentType.objects.get_for_model(Product)
        
        # Получаем права для группы
        permissions = Permission.objects.filter(content_type=content_type)
        
        # Добавляем права к группе
        added_permissions = []
        
        # Право на отмену публикации продукта
        unpublish_permission = permissions.get(codename='can_unpublish_product')
        if unpublish_permission not in group.permissions.all():
            group.permissions.add(unpublish_permission)
            added_permissions.append('can_unpublish_product')
        
        # Право на удаление любого продукта
        delete_permission = permissions.get(codename='delete_product')
        if delete_permission not in group.permissions.all():
            group.permissions.add(delete_permission)
            added_permissions.append('delete_product')
        
        if added_permissions:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Добавлены права: {", ".join(added_permissions)}'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('Все права уже назначены группе')
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                'Группа "Модератор продуктов" настроена успешно!'
            )
        )
        
        # Создаем группу "Контент-менеджер"
        content_group, created = Group.objects.get_or_create(name='Контент-менеджер')
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Группа "Контент-менеджер" создана')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Группа "Контент-менеджер" уже существует')
            )

        # Получаем контент-тип для модели BlogPost
        blog_content_type = ContentType.objects.get_for_model(BlogPost)
        
        # Получаем права для блога
        blog_permissions = Permission.objects.filter(content_type=blog_content_type)
        
        # Добавляем права к группе контент-менеджеров
        added_blog_permissions = []
        
        # Право на управление блогом
        blog_manage_permission = blog_permissions.get(codename='can_manage_blog')
        if blog_manage_permission not in content_group.permissions.all():
            content_group.permissions.add(blog_manage_permission)
            added_blog_permissions.append('can_manage_blog')
        
        # Права на создание, изменение и удаление записей блога
        blog_crud_permissions = ['add_blogpost', 'change_blogpost', 'delete_blogpost']
        for perm_codename in blog_crud_permissions:
            permission = blog_permissions.get(codename=perm_codename)
            if permission and permission not in content_group.permissions.all():
                content_group.permissions.add(permission)
                added_blog_permissions.append(perm_codename)
        
        if added_blog_permissions:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Добавлены права блога: {", ".join(added_blog_permissions)}'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('Все права блога уже назначены группе')
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                'Группа "Контент-менеджер" настроена успешно!'
            )
        )
