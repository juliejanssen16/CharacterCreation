// Get buttons and categories
const buttons = document.querySelectorAll('.button');
const categories = document.querySelectorAll('.category');

// Make sure only the right category row shows when a button is clicked
buttons.forEach(button => {
    button.addEventListener('click', () => {
        const categoryId = button.id.toLowerCase() + 'Div';

        categories.forEach(cat => {
            if (cat.id === categoryId) {
                cat.style.display = 'flex';
            } else {
                cat.style.display = 'none';
            }
        });
    });
});

// Create overlay image holders
const characterContainer = document.getElementById('characterContainer');
const layers = {
    head: null,
    face: null,
    chest: null,
    legs: null,
    shoes: null
};

// Listen for clicks on asset images
categories.forEach(category => {
    category.addEventListener('click', event => {
        if (event.target.tagName === 'IMG') {
            const img = event.target;
            const categoryType = getCategoryType(img.className);

            // Remove existing selected style
            category.querySelectorAll('img').forEach(sibling => {
                sibling.classList.remove('selected');
            });
            img.classList.add('selected');

            // Remove old overlay if it exists
            if (layers[categoryType]) {
                characterContainer.removeChild(layers[categoryType]);
            }

            // Create new overlay image
            const overlay = document.createElement('img');
            overlay.src = img.src;
            overlay.style.position = 'absolute';
            overlay.style.top = 0;
            overlay.style.left = 0;
            overlay.style.width = '100%';
            overlay.style.height = '100%';
            overlay.style.pointerEvents = 'none';

            characterContainer.appendChild(overlay);
            layers[categoryType] = overlay;
        }
    });
});

// Helper function: map class names to layer keys
function getCategoryType(className) {
    if (className.includes('Hair')) return 'head';
    if (className.includes('Face')) return 'face';
    if (className.includes('Shirt')) return 'chest';
    if (className.includes('Pants')) return 'legs';
    if (className.includes('Shoes')) return 'shoes';
    return '';
}

// Save character on submit
document.getElementById('submitButton').addEventListener('click', () => {
    const savedCharacter = {};

    Object.keys(layers).forEach(layer => {
        if (layers[layer]) {
            savedCharacter[layer] = layers[layer].src;
        }
    });

    localStorage.setItem('character', JSON.stringify(savedCharacter));
});

// Load character on page load
window.addEventListener('load', () => {
    const savedCharacter = JSON.parse(localStorage.getItem('character'));

    if (savedCharacter) {
        Object.keys(savedCharacter).forEach(layer => {
            const imgSrc = savedCharacter[layer];
            const img = Array.from(document.querySelectorAll(`#${layer}Div img`)).find(img => img.src === imgSrc);

            if (img) {
                const category = img.closest('.category');
                category.querySelectorAll('img').forEach(sibling => {
                    sibling.classList.remove('selected');
                });
                img.classList.add('selected');

                // Create overlay for saved image
                const overlay = document.createElement('img');
                overlay.src = img.src;
                overlay.style.position = 'absolute';
                overlay.style.top = 0;
                overlay.style.left = 0;
                overlay.style.width = '100%';
                overlay.style.height = '100%';
                overlay.style.pointerEvents = 'none';

                characterContainer.appendChild(overlay);
                layers[layer] = overlay;
            }
        });
    }
});
