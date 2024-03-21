<template>
    <div class="dropdown-container" tabindex="0" @click="toggleDropdown">
        <button class="dropdown-toggle">
            Select Code Example
            <font-awesome-icon :icon="isOpen ? 'angle-up' : 'angle-down'" />
        </button>
        <div class="dropdown-menu" v-if="isOpen">
            <a
                v-for="example in codeExamples"
                :key="example.name"
                class="dropdown-item"
                @click.prevent="selectExample(example.code)"
                @click="toggleDropdown"
                @mouseover="currentExplanation = example.explanation"
                @mouseleave="currentExplanation = ''"
            >
                {{ example.name }}
            </a>
        </div>
        <transition name="fade">
            <div class="tooltip" v-if="currentExplanation">
                {{ currentExplanation }}
            </div>
        </transition>
    </div>
</template>

<script>
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {faAngleDown, faAngleUp} from '@fortawesome/free-solid-svg-icons'
import {library} from '@fortawesome/fontawesome-svg-core'

library.add(faAngleDown, faAngleUp)
export default {
    name: 'CustomDropdown',
    components: {
        FontAwesomeIcon
    },
    data() {
        return {
            isOpen: false,
            currentExplanation: '',
            codeExamples: [
                {
                    name: 'Fibonacci Sequence',
                    code: `/*
  Fibonacci Sequence Printer
  This program calculates and prints the Fibonacci sequence
  numbers up to 10,000.

  You can adjust the limit by changing the value of \`limit\`.
*/

{
    // Change \`limit\` here to adjust the maximum value we print up to
    var limit = 10000;

    var a = 0; /* Initializing the first Fibonacci number */
    var b = 1; /* Initializing the second Fibonacci number */

    print_int(a); /* Printing the first Fibonacci number */

    while b < limit do {
        print_int(b);
        var next = a + b; /* Calculating the next Fibonacci number */
        a = b;
        b = next;
    }
}`,
                    explanation:
                        'Calculates and prints the Fibonacci sequence numbers up to 10,000. Adjust the `limit` variable to change the maximum value.'
                },
                {
                    name: 'Prime Number',
                    code: `/*
  Prime Number Checker
  This program checks if a number is prime and prints true or false.
  Change the value of \`n\` to test different numbers.
*/

{
    var n = 29; /* Change \`n\` here to test a different number */
    var isPrime = true;

    var i = 2;
    while i * i <= n do {
        if n % i == 0 then {
            isPrime = false;
        }
        i = i + 1;
    }

    if isPrime and n > 1 then {
        print_bool(isPrime);
    } else {
        print_bool(isPrime);
    }
}`,
                    explanation: 'Checks if the number `n` is prime and prints `true` if it is, `false` otherwise.'
                },
                {
                    name: 'Calculate Factorial',
                    code: `/*
  Factorial Calculator
  This program calculates the factorial of a number \`n\`
  and prints the result.
  Change the value of \`n\` to calculate a different factorial.
*/

{
    var n = 5; /* Change \`n\` here to calculate a different factorial */
    var result = 1;

    while n > 1 do {
        result = result * n;
        n = n - 1;
    }

    print_int(result);
}`,
                    explanation:
                        'Calculates the factorial of a number `n` and prints the result. Adjust `n` to compute a different factorial.'
                },
                {
                    name: 'Natural Numbers',
                    code: `/*
  Sum of Natural Numbers
  This program calculates the sum of the first n natural
  numbers and prints the result.
  Change the value of \`n\` to compute the sum
  for a different range.
*/

{
    // Change \`n\` here to sum a different range of natural numbers
    var n = 100;
    var sum = 0;
    var i = 1;

    while i <= n do {
        sum = sum + i;
        i = i + 1;
    }

    print_int(sum);
}`,
                    explanation:
                        'Calculates the sum of the first n natural numbers and prints the result. The range can be adjusted by changing `n`.'
                },
                {
                    name: 'GCD Euclidean',
                    code: `/*
  Greatest Common Divisor (GCD) using Euclidean Algorithm
  This program calculates the GCD of two numbers a and
  b and prints the result.
  Change the values of \`a\` and \`b\` to compute
  GCD for different pairs of numbers.
*/

{
    var a = 48; /* Change \`a\` here */
    var b = 18; /* Change \`b\` here */

    while b != 0 do {
        var temp = b;
        b = a % b;
        a = temp;
    }

    print_int(a); /* a now contains the GCD */
}`,
                    explanation:
                        'Calculates the Greatest Common Divisor (GCD) of two numbers using the Euclidean algorithm and prints the result.'
                },
                {
                    name: 'Interest Calculation',
                    code: `/*
  Simple Interest Calculator
  This program calculates the simple interest for
  given principal, rate, and time.
  Change the values of \`principal\`, \`rate\`, and \`time\` to
  compute different interests.
*/

{
    var principal = 1000; /* Principal amount */
    var rate = 5; /* Annual interest rate in percent */
    var time = 3; /* Time in years */

    /* Simple interest formula is (principal * rate * time) / 100 */
    var interest = (principal * rate * time) / 100;

    print_int(interest);
}`,
                    explanation:
                        'Calculates the simple interest for a given principal, rate, and time, and prints the result.'
                },
                {
                    name: 'Check Even or Odd',
                    code: `/*
  Check Even or Odd
  This program checks if a given number n is
  even or odd and prints "true" if even, "false" otherwise.
  Change the value of \`n\` to test different numbers.
*/

{
    var n = 4; /* Change \`n\` here to test a different number */

    if n % 2 == 0 then {
        print_bool(true);
    } else {
        print_bool(false);
    }
}`,
                    explanation:
                        'Checks if the number `n` is even or odd and prints "true" for even and "false" for odd numbers.'
                }
            ]
        }
    },
    methods: {
        toggleDropdown() {
            this.isOpen = !this.isOpen
        },
        selectExample(code) {
            this.$emit('codeSelected', code)
            this.isOpen = false
            this.currentExplanation = ''
        }
    }
}
</script>

<style scoped>
.dropdown-container {
    position: relative;
    display: inline-block;
    user-select: none;
}

.dropdown-toggle {
    background: none;
    color: var(--color-text);
    padding: 10px;
    border: #00bd7e 1px solid;
    cursor: pointer;
    outline: none;
}

.dropdown-toggle:focus {
    box-shadow: 0 0 0 2px rgba(0, 189, 126, 0.4);
}

.dropdown-menu {
    position: absolute;
    background-color: rgba(58, 58, 58, 0.9);
    min-width: 160px;
    box-shadow: 12px 12px 12px rgba(0, 0, 0, 0.2);
    z-index: 100;
}

.dropdown-item {
    color: var(--color-text);
    padding: 12px 16px;
    text-decoration: black;
    display: block;
    border-bottom: #00bd7e 1px solid;
}

.dropdown-item:hover {
    background-color: rgba(0, 189, 126, 0.8);
}

.tooltip {
    position: absolute;
    top: 0;
    transform: translateX(180px);
    background-color: rgba(0, 189, 126, 0.68);
    border: 1px solid #ccc;
    color: white;
    padding: 8px;
    margin-top: 5px;
    width: 150px;
    box-shadow: 12px 12px 12px rgba(0, 0, 0, 0.2);
    z-index: 1000;
}

@media (min-width: 1024px) {
    .tooltip {
        transform: translateX(-260px);
        width: 250px;
    }
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s ease;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}
</style>
