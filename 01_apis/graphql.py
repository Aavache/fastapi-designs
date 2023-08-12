from fastapi import FastAPI
from graphene import ObjectType, String, Schema
from graphene_fastapi import GraphQLApp

app = FastAPI()

class Query(ObjectType):
    hello = String(name=String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return f"Hello, {name}!"

schema = Schema(query=Query)

app.add_route("/", GraphQLApp(schema=schema))


'''
install

pip install fastapi graphene

send
{
  hello(name: "Alice")
}


You should receive a response like:

json
Copy code
{
  "data": {
    "hello": "Hello, Alice!"
  }
}

'''