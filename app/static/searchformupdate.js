document.addEventListener('DOMContentLoaded', (event) => {
    const md = document.getElementById('md');
    const mdOutput = document.getElementById('mdDisplay');
    updateOutput(md.value);

    md.addEventListener('input', (event) => {
        updateOutput(event.target.value);
    });
});

function updateOutput(value) {
    if (value == 100) {
        value = value + "+";
    }
    document.getElementById('mdDisplay').value = value;
}
