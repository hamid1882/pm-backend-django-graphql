import graphene
from graphene_django.types import DjangoObjectType
from .models import Organization, Project, Task

# GraphQL type definitions for our models


class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project


class TaskType(DjangoObjectType):
    class Meta:
        model = Task

# Define the Query type with fields to retrieve all organizations, projects and tasks


class Query(graphene.ObjectType):
    all_organizations = graphene.List(OrganizationType)
    all_projects = graphene.List(ProjectType)
    all_tasks = graphene.List(TaskType)

    organization_by_id = graphene.Field(OrganizationType, id=graphene.ID())
    project_by_id = graphene.Field(ProjectType, id=graphene.ID())
    task_by_id = graphene.Field(TaskType, id=graphene.ID())

    # Resolver functions for retrieving all organizations, projects and tasks
    def resolve_all_organizations(self, info):
        return Organization.objects.all()

    def resolve_all_projects(self, info):
        return Project.objects.all()

    def resolve_all_tasks(self, info):
        return Task.objects.all()

    def resolve_organization_by_id(self, info, id):
        try:
            return Organization.objects.get(pk=id)
        except Organization.DoesNotExist:
            return None

    def resolve_project_by_id(self, info, id):
        try:
            return Project.objects.get(pk=id)
        except Project.DoesNotExist:
            return None

    def resolve_task_by_id(self, info, id):
        try:
            return Task.objects.get(pk=id)
        except Task.DoesNotExist:
            return None

# Define mutations for creating, updating, and deleting organizations, projects and tasks


class CreateOrganization(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        slug = graphene.String(required=True)
        contact_email = graphene.String(required=True)

    organization = graphene.Field(OrganizationType)

    def mutate(self, info, name, slug, contact_email):
        organization = Organization(
            name=name, slug=slug, contact_email=contact_email)
        organization.save()
        return CreateOrganization(organization=organization)


class CreateProject(graphene.Mutation):
    class Arguments:
        organization_id = graphene.ID(required=True)
        name = graphene.String(required=True)
        description = graphene.String()
        status = graphene.String()
        due_date = graphene.types.datetime.Date()

    project = graphene.Field(lambda: ProjectType)

    def mutate(self, info, organization_id, name, description=None, status=None, due_date=None):
        try:
            organization = Organization.objects.get(pk=organization_id)
        except Organization.DoesNotExist:
            raise Exception(
                f"Organization with id {organization_id} not found.")

        project = Project(
            organization=organization,
            name=name,
            description=description if description is not None else "",
            status=status if status is not None else "active",
            due_date=due_date
        )
        project.save()
        return CreateProject(project=project)


class CreateTask(graphene.Mutation):
    class Arguments:
        project_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        description = graphene.String()
        status = graphene.String()
        assignee_email = graphene.String()
        due_date = graphene.types.datetime.DateTime()

    task = graphene.Field(lambda: TaskType)

    def mutate(self, info, project_id, title, description=None, status=None, assignee_email=None, due_date=None):
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise Exception(f"Project with id {project_id} not found.")

        task = Task(
            project=project,
            title=title,
            description=description if description is not None else "",
            status=status if status is not None else "todo",
            assignee_email=assignee_email if assignee_email is not None else "",
            due_date=due_date
        )
        task.save()
        return CreateTask(task=task)


class UpdateOrganization(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        slug = graphene.String()
        contact_email = graphene.String()

    organization = graphene.Field(lambda: OrganizationType)

    def mutate(self, info, id, name=None, slug=None, contact_email=None):
        try:
            organization = Organization.objects.get(pk=id)
        except Organization.DoesNotExist:
            raise Exception(f"Organization with id {id} not found.")

        if name is not None:
            organization.name = name
        if slug is not None:
            organization.slug = slug
        if contact_email is not None:
            organization.contact_email = contact_email

        organization.save()
        return UpdateOrganization(organization=organization)


class UpdateProject(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        organization_id = graphene.ID()
        name = graphene.String()
        description = graphene.String()
        status = graphene.String()
        due_date = graphene.types.datetime.Date()

    project = graphene.Field(lambda: ProjectType)

    def mutate(self, info, id, organization_id=None, name=None, description=None, status=None, due_date=None):
        try:
            project = Project.objects.get(pk=id)
        except Project.DoesNotExist:
            raise Exception(f"Project with id {id} not found.")

        if organization_id is not None:
            try:
                organization = Organization.objects.get(pk=organization_id)
                project.organization = organization
            except Organization.DoesNotExist:
                raise Exception(
                    f"Organization with id {organization_id} not found.")
        if name is not None:
            project.name = name
        if description is not None:
            project.description = description
        if status is not None:
            project.status = status
        if due_date is not None:
            project.due_date = due_date

        project.save()
        return UpdateProject(project=project)


class UpdateTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        project_id = graphene.ID()
        title = graphene.String()
        description = graphene.String()
        status = graphene.String()
        assignee_email = graphene.String()
        due_date = graphene.types.datetime.DateTime()

    task = graphene.Field(lambda: TaskType)

    def mutate(self, info, id, project_id=None, title=None, description=None, status=None, assignee_email=None, due_date=None):
        try:
            task = Task.objects.get(pk=id)
        except Task.DoesNotExist:
            raise Exception(f"Task with id {id} not found.")

        if project_id is not None:
            try:
                project = Project.objects.get(pk=project_id)
                task.project = project
            except Project.DoesNotExist:
                raise Exception(f"Project with id {project_id} not found.")
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if assignee_email is not None:
            task.assignee_email = assignee_email
        if due_date is not None:
            task.due_date = due_date

        task.save()
        return UpdateTask(task=task)


class DeleteOrganization(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            organization = Organization.objects.get(pk=id)
            organization.delete()
            return DeleteOrganization(success=True, message=f"Organization with ID {id} deleted.")
        except Organization.DoesNotExist:
            return DeleteOrganization(success=False, message=f"Organization with ID {id} not found.")


class DeleteProject(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            project = Project.objects.get(pk=id)
            project.delete()
            return DeleteProject(success=True, message=f"Project with ID {id} deleted.")
        except Project.DoesNotExist:
            return DeleteProject(success=False, message=f"Project with ID {id} not found.")


class DeleteTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            task = Task.objects.get(pk=id)
            task.delete()
            return DeleteTask(success=True, message=f"Task with ID {id} deleted.")
        except Task.DoesNotExist:
            return DeleteTask(success=False, message=f"Task with ID {id} not found.")

# Define the Mutation type with fields for all defined mutations


class Mutation(graphene.ObjectType):
    create_organization = CreateOrganization.Field()
    update_organization = UpdateOrganization.Field()
    delete_organization = DeleteOrganization.Field()
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()


# Define the schema with the Query and Mutation types
schema = graphene.Schema(query=Query, mutation=Mutation)
