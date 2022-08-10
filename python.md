# Python

- String, Numbers, Booleans are primitive types
- Primitive types are immutable
- \# means comment
- f"{var}" for printing variable value as string. It is like `${}` in javascript
- // gives the integer result of division
- There is no increment or decrement operator
- There is no constant in python
- input()- function to take user input
- Python is strongly typed language, unlike JavaScript. It doesn't know how to convert between
types automatically
- int() - type conversion function
- falsy value: "", 0, [], None(null)
- and, or, not: Conditional operators
- Comparison operators can be written as we write in math
- Ternary operator: 
- There are only for and while loop
- Tuple

Function signature

def function name (arg, arg) -> return type:
  body

```python
  def function name (\*arg):
    this function is taking a tuple as argument
  call this function (1,2,3,4) : The arguments will be passed as tuple
```

```python
  def function name(\*\*arg):
    This function argumetn is passed as dictionary
```

- Variable scope: function scope and global scope

## Data Model

### Objects, values and types

**Type hierarchy**

- None
- NotImplemented
- Ellipsis
- numbers:Number
- numbers:Integral 
  - Integers(int)
  - Booleans(bool): 0 and 1 as integer. When converted to string prints "True"
                    and "False"
- numbers:Real: Float
- numbers:Complex: The real and imaginary parts of a complex number z can be
                    retrieved through the read-only attributes z.real and
                    z.imag.
- Sequence: Finite ordered sets indexed by non-negative numbers.
  - Immutable sequence: The object can't change
    - Strings: There is no `char` type. In stead a `String` of 1 length.
    - Tuples
    - Bytes
  - Mutable sequence:
    - List
    - Byte Arrays
- Set type
  - Sets: Mutable set
  - Frozen sets: Immutable set. Created by `frozenset()`. This is hashable so
                    can be used as dictionary key.
- Mappings: Represents finite sets of object indexed by arbitrary index sets.
  - Dictionary: These represent finite sets of objects indexed by nearly
                    arbitrary values.  The only types of values not acceptable
                    as keys are values containing lists or dictionaries or other
                    mutable types that are compared by value rather than by
                    object identity, the reason being that the efficient
                    implementation of dictionaries requires a key’s hash value
                    to remain constant.  Numeric types used for keys obey the
                    normal rules for numeric comparison: if two numbers compare
                    equal (e.g., 1 and 1.0) then they can be used
                    interchangeably to index the same dictionary entry.
                    
                    Dictionaries preserve insertion order, meaning that keys
                    will be produced in the same order they were added
                    sequentially over the dictionary. Replacing an existing key
                    does not change the order, however removing a key and
                    re-inserting it will add it to the end instead of keeping
                    its old place.
- Callable type: These are the types to which the function call operation can be
applied.

## Classes

1. Classes are created at runtime and can be modified after they are created.
2. Built in types can be used for extension by user
3. Built in operators can be redifined for class instances
4. Mutable objects are passed as pointers. So if a function makes changes to the
   object the caller will see the change
5. Modules are objects. These objects have attributes which can be read-only or
   writable. Writable attributes can be assigned or deleted using `del` keyword.

#### Scopes and Namespaces

[Read here](https://docs.python.org/3/tutorial/classes.html#python-scopes-and-namespaces)

#### Creation of class

- When a class definition is entered, a new namespace is created and used as the
local scope
- When the class definition is left normally, a class object is created. This is
a wrapper around the contents of namespace created by class definition

#### Class objects

- Class objects support two kinds of operations: attribute references and instantiation
- Attribute reference use the `.` operator to access the attributes. Like
`MyClass.variable`. This way we can assign values to attributes. The methods of
a class is also an attribute.
- The instantiation operation creates an empty object. If you want to
instantiate a class to a customized initial state, use the `__init()__` method.

#### Instance objects

- Only supported operations are attribute reference
- There are two kind of attribute names: data and method
- Data attributes need not to be declared within the class. We can just add a
data attribute to a class bu assigning a value to it. 

for example- If I have the following class

```python
class MyClass:
  a=10

myClass = MyClass()
```

I can add a data attribute by following code

```python
myClass.b=20
```
This will make the variable `b` a data attribute of the object `myClass`.

- A method is a function that belongs to an object. The following example will
make it clear

```python
class MyClass:
  def sum(self, a,b):
    return a+b

myClass = MyClass()
```

In the above example, the `MyClass.sum` is of type `function` where as the
`myClass.sum` is of type `method`.

- Methods are objects instantiated from function

#### Method objects

When we write `myClass.sum(2,5)` the following happens-

- The class object of `myClass` is searched for an attribute `sum`. In this case
the class object is `MyClass`
- If the attribute is found and it is function object, a method object is
created by packing the pointer to instance object(`myClass`) and the function
object in an abstract object.
- When we call the method object with arguments, a new list of arguments is
created from the instance object and the argument list and the function object
is called with this argument.

So, the above function call correspond to `MyClass.sum(myClass,2,5))`. A method
is called when it is bound. The bounding is done by `()` operator.


