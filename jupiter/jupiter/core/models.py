from django.contrib.postgres.fields import JSONField
from django.conf import settings
from django.db import models


import docker


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=150)
    dockerfile = models.TextField('Dockerfile', blank=True, null=True)
    data = JSONField(default={}, blank=True, null=True)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"

    def __str__(self):
        return self.name


class UserService(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Usuário",
        on_delete=models.PROTECT
    )
    service = models.ForeignKey(Service)
    address = models.CharField('Endereço', max_length=50, unique=True)
    data = JSONField(default={}, blank=True, null=True)

    @property
    def url(self):
        return "{0}.{1}".format(self.address, settings.URL_SUFFIX)

    def get_container(self):
        try:
            client = docker.from_env()
            container = client.containers.get(self.data.get("container_id"))
            return container
        except:
            return False

    def save(self, *args, **kwargs):
        if not self.data.get("created",False):
            client = settings.DOCKER_CLIENT
            image = self.service.data.get('image')
            command = self.service.data.get('command')
            mem_limit = self.data.get('mem_limit', settings.MEM_LIMIT)
            ports = self.service.data.get('ports')
            
            env = {}
            env.update(self.data.get('environment', {}))
            env.update(self.service.data.get('environment', {}))
            env.update({"VIRTUAL_HOST": self.url})
            
            container = client.containers.run(
                image=image, 
                command=command, 
                mem_limit=mem_limit,
                environment=env,
                #ports=ports,
                publish_all_ports=False,
                detach=True
            )
            
            # container.start()
            self.data.update({"container_id":container.id})
            self.data.update({"created":True})
        super(UserService, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        container = self.get_container()
        if container.status == "running" or container.status == "paused":
            container.kill()
        container.remove()
        super(UserService, self).delete(*args, **kwargs)


    @property
    def status(self):
        container = self.get_container()
        return container.status

    def pause(self):
        try:
            container = self.get_container()
            container.pause()
            return True
        except:
            return False

    def unpause(self):
        try:
            container = self.get_container()
            container.unpause()
            return True
        except:
            return False

    def stop(self):
        try:
            container = self.get_container()
            container.stop()
            return True
        except:
            return False

    def kill(self):
        try:
            container = self.get_container()
            container.kill()
            return True
        except:
            return False

    def start(self):
        try:
            container = self.get_container()
            container.start()
            return True
        except:
            return False

    class Meta:
        verbose_name = "Serviço do usuário"
        verbose_name_plural = "Serviços do usuário"

    def __str__(self):
        return self.service.name