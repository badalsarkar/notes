# JAVASCRIPT


## Promise

- It is an object
- It is a proxy value returned by an asynchronous function
- In stead of returning the final value, the asynchronous functions returns a promise to supply the value at some
point in future. 

```javascript
var promiseObj= new Promise(executor);
//executor is a function,  provided by the programmer. 
//This function is executed during the construction of promise object
//The signature of executor is following

function(resolutionFunc, rejectionFunc){
    //typically some async operation
    //the operation is terminated either by resolutionFunc() or by rejectionFunc()
    //both of these functions have a data parameter like resolutionFunc(data) and rejectionFunc(data)
    //this data is passed back to the promiseObj
}
```

- The promise constructor generates a function for resolutionFunc and a function for rejectionFunc. ResolutionFunc can
be used to terminate the promise with fulfilled status and the rejectionFunc can be used to terminate the promise with
rejected status. The executor has no meaningful return value. 

- When we invoke the **then()** method of promiseObj we get the data passed from the resolutionFunc or rejectionFunc. 
This data is then passed to the handler function as parameter. 


### then() 

```javascript
Promise.then(onFulfilled[, onRejected]);
```

- This function returns a promise.
- The function takes two arguments- a) callback for success of promise b) callback function for failure of promise
- Once a promise is successful or rejected, the respective callback is called asynchronously. 
- The return value of then() depends on some factors. See the [link](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/then)
- Promise object has three status- pending, fulfilled, rejected.
- We can attach handlers (functions) for each state.
- We attach handlers using the promise's **then** method.
- Both **then() and catch()** returns promise


### Async/ Await

Source: (https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Async_await)

- A function defined as **async** always returns a promise. A promise is a built in object in Javascript. I has several
methods and properties. When we call an async function, we get this promise back and the function starts processing in 
the background. We can check the status of the promise object that we received from the function, to know the status of 
the function. Promise also provides several methods to attach handler for different status of the object. In async function
a promise object is constructed from the code block. 

- Await keyword makes your code wait for the fulfillment of the promise. 
- You can use **await** keyword with any function that returns a promise. We can say that you await on the promise. 
Therefore, you can use await with any variable that holds a promise. 
```javascript
const timeoutPromise1 = timeoutPromise(3000);
const timeoutPromise2 = timeoutPromise(3000);
const timeoutPromise3 = timeoutPromise(3000);

await timeoutPromise1;
await timeoutPromise2;
await timeoutPromise3;
```


## Set 

(https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set)

## Testing

## Memory management in JavaScript

(https://developer.mozilla.org/en-US/docs/Web/JavaScript/Memory_Management)

Question: How is javascript's array implemented?


## Function overloading in Javascript

[Read here](https://stackoverflow.com/questions/10855908/how-to-overload-functions-in-javascript/10855939)


## Useful resources

[Mocha and Assert](https://www.digitalocean.com/community/tutorials/how-to-test-a-node-js-module-with-mocha-and-assert)

