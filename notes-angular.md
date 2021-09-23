# Learning Angular

# Table of Contents

- [Learning Angular](#learning-angular)
- [Table of Contents](#table-of-contents)
  - [Angular concepts](#angular-concepts)
    - [Modules](#modules)
    - [Decorators](#decorators)
    - [Components](#components)
    - [Template](#template)
    - [Directives](#directives)
    - [Data Binding](#data-binding)
  - [Forms](#forms)
    - [Differences between two form types](#differences-between-two-form-types)
    - [Common Foundation between Two Types](#common-foundation-between-two-types)
      - [What is FormControl](#what-is-formcontrol)
      - [What is FormGroup](#what-is-formgroup)
      - [What is FormArray](#what-is-formarray)
      - [What is ControlValueAccessor](#what-is-controlvalueaccessor)
    - [Form Model Setup](#form-model-setup)
      - [Form Model in Reactive Form](#form-model-in-reactive-form)
      - [Form model in template driven form](#form-model-in-template-driven-form)
    - [Data Flow in Forms](#data-flow-in-forms)
    - [Form Validation](#form-validation)
      - [Validating template driven form](#validating-template-driven-form)

## Angular concepts

### Modules

ksfjksdfk

### Decorators

Decorators provides type and metadata. Angular uses them to process the class
in a module.

NgModule is a decorator which marks a class as NgModule and supplies
configuration metadata.

### Components

Angular components are regular Javascript classes. But for Angular to treat
these classes as component, we need to mark these classes with decorators. As
mentioned before a decorator provides type information and metadata. For
component the `@Component()` decorator is used. This component provides the
template to display the data, and other metadata for Angular. In Angular the
root component is the app component.

### Template

This is the view of a component. This is an HTML file with Angular markup.
Angular markups modify the view before rendering to display.

### Directives

Angular directives provides application logic to the template.

ngModel is a directive. It creates FormControl instance and binds it to the form
control element.

### Data Binding

Binds component data to the view. This binding can be done in two ways:

- Property binding: This allows us to add application to the view.
- Event binding: Synchronizes application with the user input in browser.

*Service Class*
The application data and logic that is not related to a specific component, are
put into service class. The idea is that these classes are used by many
components. Services classes are defined as injectable which means they can be
injected as dependency (DI) into other classes. Therefor, these classes are
decorated with `@Injectable` decorator.

*Routing*
Provides routing functionality.

## Forms

Two different approach-

1. Reactive: More robust and scalable.
2. Template driven: User for simple form.

### Differences between two form types

| Parameter |  Reactive |  Template Driven |
|:----------|:----------|:-----------------|
|Setup(form model)|Created in component class|Created by directives|
|Data model|Structured|Unstructured|
|Predictability|Synchronous|Asynchronous|
|Form validation|Functions|Directives|
|Mutability|Immutable|Mutable|
|Scalability|Low level API access|Abstraction on top of APIs|

### Common Foundation between Two Types

- FormControl tracks the value and validation status of an individual form
control.
- FormGroup tracks the same values and status for a collection of form
controls.
- FormArray tracks the same values and status for an array of form controls.
- ControlValueAccessor creates a bridge between Angular FormControl instances
and native DOM elements.

#### What is FormControl

[FormControl](https://angular.io/api/forms/FormControl) is a class defined in
Angular. It tracks the values and validation status of an individual [form
control.](https://www.w3.org/TR/html4/interact/forms.html#h-17.2). We need to
instantiate a FormControl object and attach it to the control that we want to
track and validate.

A control is an especial element of a form(checkboxes, radio buttons, menus
    etc). Users generally complete a form by modifying its controls. A control's
control name is defined by the "name" attribute. A control has initial value and
current value. Initial value is defined by the "value" attribute except textarea
control whose initial value is defined by "contents".  

For more details about different types of control read [here](https://www.w3.org/TR/html4/interact/forms.html#h-17.2).

For more details about FormControl class read [here](https://angular.io/api/forms/FormControl)

#### What is FormGroup

This is a class defined in Angular. It tracks the value and validity state of a
group of form control. If any of the child control is invalid, the whole group
becomes invalid.

#### What is FormArray

This is a class defined in Angular. It tracks the value and validity of an array
of FormControl, FormGroup or FormArray instanes. If one of the control of the
array is invalid, the whole array becomes invalid.

#### What is ControlValueAccessor

This is an interface defined in Angular. It bridges between Angular forms API
and native element in DOM.

### Form Model Setup

Both reactive and template driven forms use form model to track the value
changes between Angular form and input elements.

#### Form Model in Reactive Form

In reactive form the source of truth is the form model. So, we create a form
model in the component class. The form model can be an instance of FormControl.
Now that we have a model, we need to attach it with a form element (input,
    textarea etc) so that the value and validity of the element can be tracked
by Angular. This is done using a directive called **DefaultValueAccessor**. This
is the default ControlValueAccessor which writes value to form element and
listens for changes in the input elements.

```angular

import { Component } from '@angular/core';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-reactive-favorite-color',
  template: `
    //attach the form model with an form element
    //here [formControl] is the DefaultValueAccessor for input element
    Favorite Color: <input type="text" [formControl]="favoriteColorControl">
  `
})
export class FavoriteColorComponent {
  //create an instance of FormControl to be used as form model
  favoriteColorControl = new FormControl('');
}

```

#### Form model in template driven form

In template driven form the source of truth is the template which is defined in
the component class. The FormControl instance is not created by programmer.
Rather, NgModel directive creates and manages the FormControl instance. So, it
is simple but we don't have direct access to the FormControl instance.

```angular
import { Component } from '@angular/core';

@Component({
  selector: 'app-template-favorite-color',
  template: `
    //attach the form model favoriteColor using NgModel directive
    Favorite Color: <input type="text" [(ngModel)]="favoriteColor">
  `
})
export class FavoriteColorComponent {
  //define form model
  favoriteColor = '';
}
```

### Data Flow in Forms

### Form Validation

There are built in validator and we can also define custom validator.

#### Validating template driven form

The validation is done using regular html validation attribute. Angular attaches
these attributes with the directives. Every time the value changes, Angular runs
the validators and generates either a list of validation errors or null.




