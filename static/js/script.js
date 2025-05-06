const button = document.getElementById('notificationButton');
const dropdown = document.getElementById('notificationDropdown');
const wrapper = document.getElementById('notificationWrapper');

function toggleDropdown(forceState = null) {
    if (forceState === true) {
        dropdown.classList.remove('hidden');
    } else if (forceState === false) {
        dropdown.classList.add('hidden');
    } else {
        dropdown.classList.toggle('hidden');
    }
}

button.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleDropdown();
});

document.addEventListener('click', (e) => {
    if (!wrapper.contains(e.target)) {
        toggleDropdown(false);
    }
});