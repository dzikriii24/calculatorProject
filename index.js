const displayHistory = document.querySelector(".history");
const display = document.querySelector(".input");
const tempResult = document.querySelector(".return");
const numbers = document.querySelectorAll(".number");
const operations = document.querySelectorAll(".operation");
const equal = document.querySelector(".equal");
const clearAll = document.querySelector(".clear-all");
const clearLast = document.querySelector(".clear");
const hovers = document.querySelector(".button");

let disNum = ""; 
let dis2Num = ""; 
let result = null;
let lastOperation = "";
let haveDot = false ;

numbers.forEach((number) => {
    number.addEventListener("click", (e) => {
        if (e.target.innerText === "." && !haveDot) {
            console.log(e.target.innerText)
            haveDot = true
        } else if (e.target.innerText === "." && haveDot) {
            return;
        }
        dis2Num += e.target.innerText;
        display.innerText = dis2Num;
    })
});

operations.forEach ((operation) => {
    operation.addEventListener("click", (e) => {
        if (!dis2Num) return;
        haveDot = false;
        const operationName = e.target.innerText;
        if (disNum && dis2Num && lastOperation) {
            mathOperation()
        } else {
            result = parseFloat (dis2Num);
        }
        clearVar(operationName)
        lastOperation = operationName
    })
})
function clearVar(name = "") {
    disNum += dis2Num + " " + name + " ";
    displayHistory.innerText = disNum;
    display.innerText = "" ;
    dis2Num = ""
    tempResult.innerText = result;
}
function mathOperation () {
    if (lastOperation === "x") {
        result = parseFloat(result) * parseFloat(dis2Num)
    } else if(lastOperation === "+") {
        result = parseFloat(result) + parseFloat(dis2Num)
    } else if(lastOperation === "-") {
        result = parseFloat(result) - parseFloat(dis2Num)
    } else if(lastOperation === "/") {
        result = parseFloat(result) / parseFloat(dis2Num)
    } else if(lastOperation === "%") {
        result = parseFloat(result) % parseFloat(dis2Num)
    } 
}

equal.addEventListener("click", () => {
    if (!disNum || !dis2Num) return;
    haveDot = false;
    mathOperation()
    clearVar();
    display.innerText = result;
    tempResult.innerText = "";
    dis2Num = result;
    disNum = "";
});

clearAll.addEventListener("click", () => {
    disNum = "";
    dis2Num = "";
    haveDot = false;
    displayHistory.innerText = ""
    display.innerText = ""
    tempResult.innerText = ""
    result = ""
    lastOperation = ""
})

clearLast.addEventListener("click", () => {
    display.innerText = ""
    dis2Num = ""
})

window.addEventListener("keydown", (e) => {
    if (
        e.key === "0" ||
        e.key === "1" ||
        e.key === "2" ||
        e.key === "3" ||
        e.key === "4" ||
        e.key === "5" ||
        e.key === "6" ||
        e.key === "7" ||
        e.key === "8" ||
        e.key === "9" 
    ) {
        clickButton(e.key);
    } else if (e.key === "+" || e.key === "-" || e.key === "/" || e.key === "%") {
        clickOperation(e.key);
    } else if (e.key === "*" || e.key === "x") {
        clickOperation("x")
    } else if (e.key === "Enter" || e.key === "=") {
        clickEqual();
    } else if (e.key === "Backspace") {
        clickClear()
    }
})

function clickButton(key) {
    numbers.forEach((button) => {
        if (button.innerText === key) {
            button.click()
        }
    })
}

function clickOperation(key) {
    operations.forEach((operation) => {
        if(operation.innerText === key) {
            operation.click()
        }
    })
}

function clickEqual() {
    equal.click()
}

function clickClear() {
    clearAll.click()
}

