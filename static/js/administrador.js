const list = document.getElementById('list');

list.addEventListener('wheel', (event) => {
  const scrollAmount = Math.sign(event.deltaY) * 5;
  list.scrollTop += scrollAmount;
});