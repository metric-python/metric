## #Resource
Let's imagine your app is one huge beverage factory with much smaller brewery process, pipe to flowing down the water, insulation tank etc. So the resource is much like the smaller brewery process in your app, this resource work between the traffic and the view of your application. Let's get straight to the resource in Metric framework.

---

## #Create the Resources
### **#Basic Resources**
Take a look at this sample code of Metric resources

```python
from metric.app.resource import Resource
from metric.db.schemas import Schemas


class Users(Resource, Schemas):
    """
    Resources Users
    """
    def get(self):
        """
        Show the all users from model Users
        """
        users = self.model.Users()
        return users.all().result(), 200
```

If you look at the example code above, we have the class resources called **Users** with 2 parents class which is *Resource* and *Schemas*, the parent class resource is defined the *Users* as resources class and for the schemas is purposely called the model from ORM Schema for *Users* resource to accessing the models it needed.

---
**NOTE:**
Schemas class are not required to Resources, but it required to called the Models from ORM
---

### **#Request & Validation**
Resource request and it's validation is included within the resource base class, so whenever you want to strict and rules the resource request just called the validation and define the parameters.

```python
from metric.app.resource import Resource
from metric.db.schemas import Schemas


class Users(Resource, Schemas):
    """
    Resources Users
    """
    def post(self):
        """
        Post/insert a user to database
        """
        users = self.model.Users()
        request = self.requests
        validation = self.validation(
            name='required',
            username='required',
            email='required,email',
            password='required'
        )
        
        if validation['errors'] is not None:
            return validation['error'], 422
        else:
            try:
                users.add(**request)
                return {
                    "id": users.id,
                    "name": users.name,
                    "email": users.email,
                    "username": users.username
                }, 200
            except:
                return {"error": "internal_server_error"}, 500

```

From the code above, the resource define validation, request and model and then the first condition is the validation error appear or not, if it's not then the resource will proceed to add the record for the model based on the request that has been filtered.