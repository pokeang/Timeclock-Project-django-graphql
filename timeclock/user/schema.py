from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_jwt.shortcuts import get_token
from graphql_jwt.decorators import login_required
import graphene
import graphql_jwt


# Make models available to graphene.Field
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

## Mutation: Create User
# We want to return:
# - The new `user` entry
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
      
        token = get_token(user)
        
        return CreateUser(user=user, token=token)


# Finalize creating mutation for schema
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
  
## Query: Find users
# Demonstrates auth block on seeing myself - only if I'm logged in
class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    
    @login_required
    def resolve_me(self, info):
        user = info.context.user

        # Check to to ensure you're signed-in to see yourself
        if user.is_anonymous:
            raise Exception('Authentication Failure: Your must be signed in')
        return user
    
# Create schema
schema = graphene.Schema(query=Query, mutation=Mutation)
