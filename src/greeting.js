function getGreeting(name = "World") {
  return `Hello, ${name}!`;
}

console.log(getGreeting());

function sayGoodbye() {
  return 'Goodbye!';
}

export { getGreeting, sayGoodbye };