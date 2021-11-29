# React

# Table of Contents

- [React](#react)
- [Table of Contents](#table-of-contents)
  - [Setting up REACT](#setting-up-react)
    - [Folder structure](#folder-structure)
    - [Type of component](#type-of-component)
      - [Props](#props)
      - [Children props](#children-props)
      - [State](#state)
      - [Hooks](#hooks)
    - [Components and Props](#components-and-props)
    - [State and Lifecycle](#state-and-lifecycle)
      - [Event Handler](#event-handler)
      - [Conditional Rendering](#conditional-rendering)
      - [Lists and Keys](#lists-and-keys)
  - [Forms](#forms)
    - [useRef](#useref)
      - [Sources](#sources)

We can use HTML to structure static content. If we want to create a dynamic
structure, we need to be able to change the HTML elements somehow. For example,
  if we want to display a table with dynamic data, we need to parse the data and
  generate table row with the data and then display the table. We can do it
  using a Javascript function which will take the data as argument and return
  some HTML table row element with the data. We can then attach the returned
  result to the DOM.

So far my understanding is- React also does similar things, creating HTML
elements and attaching in DOM.

To create elements it uses two methods- function and class(details are below).
To attach elements to DOM React provides a function ReactDom.render(). It uses
React-DOM which is a virtual DOM (detalis are below).

- JSX = Javascript + XML HTML like syntax inside Javascript file.  React
uses JSX but it is not mandatory. Using it helps to read the code and find many
errors.

- Rendering Element Elements are the smallest building blocks of React apps.

React elements are [immutable](https://en.wikipedia.org/wiki/Immutable_object)
[(more about mutability)](https://github.com/badalsarkar/Software-Engineering-Concepts/blob/master/mutability/mutability.md).
They can't be changed once created.  The only way to update them is to create
new element.  To render an element, you need to pass two things to
ReactDOM.render method- the element itself and the DOM node where to render the
element.

```Javascript
const element= <h1>Hello, world</h1>; 
ReactDOM.render(element, document.getElementById('root')); 
```

## Setting up REACT

- You can add React CDN and Babel CDN and the srcipt in the HTML file. THis is
not the best way as it is difficult to maintain.

- user the "create-react-app" command. This will setup the development
environment for you.  The command is `npx create-react-app name-of-the-app}`.
Once you installed, run "npm start". This will run the app in localhost 3000.

- React Developer Tools- A google chrome plugin that helps debugging react in
chrome dev tools.

### Folder structure

- Public folder: contains the html file with "root" element. All react
components are added in the root element

- src folder: this folder contains all our React code.

### Type of component

- Class component: These are custom component defined as class. A class
component must include a render() method and can only return one
parent element.
- Simple component: This is a function. This component does not use the "class"
keyword. The function returns JSX code.

#### Props

React handles data with properties (Props) and state. Props are
read-only for components. So, components can't change the Props value.

#### Children props

Anything between opening and closing tag of component. It is accessed by the
keyword 'children'.


#### State

This is data that can be saved and modified without being added to
the database. For example, items added and removed from shopping cart.

#### Hooks

- name starts with 'use..'
- Component name must be uppercase
- must be in function/component body
- cannot call conditionally
- with object use spread operator to override a specific property.

**useEffect hook**

work outside of the component. By default runs after every re-render.
For data fetching we can use it. This hook takes two parameters. The first one
is a call back function that defines the functionality that will be run by
useEffect and the second one is an array that defines dependencies. If we pass
an empty array as the second argument, useEffect will only run at the first
render. If we want run useEffect if the value of a certain object change, we
need to put it in the array. We can have as many useEffect as we want.

**Clean up function with useEffect**

window object.

Put the clean up logic inside a return statement which should return a callback.
This is useful for conditional rendering of components.

- useEffect's first argument can't be async-await. Because useEffect's return
statement returns the clean up function. But async functions return a promise.

**useRef**

- Doesn't trigger re-render.
- Used to target dom element

**useReducer**

This hook accepts a function that will manipulate the state.

### Components and Props

Components are re-usable items. They are made of
elements. They are Javascript function take input and return React element
describing what should appear in the screen.

Props are the argument that is passed to component as JSX attributes. When React
sees an element representing a user defined component, it passes the JSX
attribute to this component as single object. this object is called "props".

Always start component name with capital letter. Component with lowercase letter
is treated as DOM tags.This is realted to JSX. To learn more about the reasoning
[click here](https://reactjs.org/docs/jsx-in-depth.html#user-defined-components-must-be-capitalized)

### State and Lifecycle

State variables are private to the component and mutable. To use state
variable, we need to declare the component as class. We need to add a
constructor and call the base constructor with the props

When a component is added to the DOM it is called mounting and when it is
removed from the DOM it is called unmounting.  We can run special function
during mounting and unmounting. Function named "componentDidMount()" is called
while mounting.  And "componentWillUnmount()" is called during unmounting.

setState() function triggers an update in the UI.

**State update may be asynchronous.** This means that React may batch multiple
setState function call together for execution for performance reason. Because
setState is an asynchronous function, we shouldn't depend on the previous state
to calculate or derive next state.

#### Event Handler

#### Conditional Rendering

Based on the different state value we can render different component. 

#### Lists and Keys
- the use of map() method.
- use keys in an array of items

## Forms

- Controlled Component
- event.preventDefault
- onChange event to attach form input value to the state

### useRef

Targeting the dom element.
- Doesn't trigger re-render
- Preserve value

#### Sources
1. https://www.taniarascia.com/getting-started-with-react/
2. https://github.com/uberVU/react-guide/blob/master/props-vs-state.md
3. https://lucybain.com/blog/2016/react-state-vs-pros/
