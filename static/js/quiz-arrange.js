document.addEventListener('DOMContentLoaded', function () {
    var answerEl = document.getElementById('arrange-answer');
    var bankEl = document.getElementById('arrange-bank');
    if (!answerEl || !bankEl) return;

    var chosenInput = document.getElementById('arrange-chosen');
    var submitBtn = document.getElementById('arrange-submit');
    var picked = [];

    function render() {
        answerEl.innerHTML = '';
        picked.forEach(function (tile) {
            var chip = document.createElement('button');
            chip.type = 'button';
            chip.className = 'quiz-word-chip';
            chip.textContent = tile.dataset.word;
            chip.addEventListener('click', function () {
                tile.disabled = false;
                picked = picked.filter(function (t) { return t !== tile; });
                render();
            });
            answerEl.appendChild(chip);
        });
        chosenInput.value = picked.map(function (t) { return t.dataset.word; }).join(' ');
        submitBtn.disabled = picked.length === 0;
    }

    Array.prototype.forEach.call(bankEl.querySelectorAll('.quiz-word-tile'), function (tile) {
        tile.addEventListener('click', function () {
            if (tile.disabled) return;
            tile.disabled = true;
            picked.push(tile);
            render();
        });
    });
});
