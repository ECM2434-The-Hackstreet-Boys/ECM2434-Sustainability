document.addEventListener("DOMContentLoaded", async function () {
    const gameContainer = document.getElementById('game-container');
    const gameWrapper = document.getElementById('game-wrapper');

    if (!gameContainer) {
        console.error("The game container element was not found!");
        return;
    }

    // Create a new Pixi application
    const app = new PIXI.Application

    const TILE_WIDTH = 64; // Width of a single tile
    const TILE_HEIGHT = 32; // Height of a single tile
    const GRID_ROWS = 10;
    const GRID_COLS = 10;


    await app.init({
        width: 800,  // Canvas width
        height: 800, // Canvas height
        backgroundColor: 0x1099bb, // Background color
    });

    // Append the Pixi canvas to the game container div
    gameContainer.appendChild(app.view);


    // Create a container to hold the grid
    const gridContainer = new PIXI.Container();
    gridContainer.x = app.renderer.width / 2; // Center the grid horizontally
    gridContainer.y = 100; // Offset the grid vertically (you can adjust this)
    app.stage.addChild(gridContainer);

    // Loop through rows and columns to create the isometric grid
    for (let row = 0; row < GRID_ROWS; row++) {
        for (let col = 0; col < GRID_COLS; col++) {
            // Calculate position of each tile in isometric space
            const x = (col - row) * (TILE_WIDTH / 2);
            const y = (col + row) * (TILE_HEIGHT / 2);

            // Create the tile shape using PIXI.Graphics
            let tile = new PIXI.Graphics();
            tile.beginFill(0xffffff); // White tile color
            tile.lineStyle(1, 0x000000); // Black border
            tile.moveTo(0, TILE_HEIGHT / 2); // Start from the top-left corner
            tile.lineTo(TILE_WIDTH / 2, 0);  // Top-middle corner
            tile.lineTo(TILE_WIDTH, TILE_HEIGHT / 2);  // Top-right corner
            tile.lineTo(TILE_WIDTH / 2, TILE_HEIGHT);  // Bottom-right corner
            tile.lineTo(0, TILE_HEIGHT / 2); // Bottom-left corner
            tile.endFill();

            // Position the tile in isometric space
            tile.x = x;
            tile.y = y;
            tile.interactive = true; // Make tile clickable
            tile.buttonMode = true;  // Change cursor to pointer on hover

            // Click event to change the tile's color
            tile.on("click", () => {
                tile.tint = Math.random() * 0xffffff; // Change color on click
            });

            // Add the tile to the grid container
            gridContainer.addChild(tile);
        }
    }

    // Implement drag functionality
    let isDragging = false;
    let lastX = 0, lastY = 0;
    let wrapperWidth = gameWrapper.clientWidth;
    let wrapperHeight = gameWrapper.clientHeight;
    let containerWidth = gameContainer.clientWidth;
    let containerHeight = gameContainer.clientHeight;

    // Function to start dragging
    function startDrag(x, y) {
        isDragging = true;
        lastX = x;
        lastY = y;
        gameWrapper.style.cursor = 'grabbing'; // Change cursor when dragging starts
    }

    // Function to move the canvas
    function moveDrag(x, y) {
        if (isDragging) {
            const dx = x - lastX;
            const dy = y - lastY;

            let newLeft = gameContainer.offsetLeft + dx;
            let newTop = gameContainer.offsetTop + dy;

            // Prevent moving too far to the right or left
            newLeft = Math.min(0, Math.max(wrapperWidth - containerWidth, newLeft));

            // Prevent moving too far up or down
            newTop = Math.min(0, Math.max(wrapperHeight - containerHeight, newTop));

            // Apply the new position
            gameContainer.style.left = newLeft + 'px';
            gameContainer.style.top = newTop + 'px';

            lastX = x;
            lastY = y;
        }
    }

    // Function to stop dragging
    function stopDrag() {
        isDragging = false;
        gameWrapper.style.cursor = 'grab'; // Reset cursor when dragging stops
    }

    // ** Mouse Events **
    gameWrapper.addEventListener('mousedown', (e) => startDrag(e.pageX, e.pageY));
    gameWrapper.addEventListener('mousemove', (e) => moveDrag(e.pageX, e.pageY));
    gameWrapper.addEventListener('mouseup', stopDrag);
    gameWrapper.addEventListener('mouseleave', stopDrag);

    // ** Touch Events **
    gameWrapper.addEventListener('touchstart', (e) => {
        const touch = e.touches[0];
        startDrag(touch.pageX, touch.pageY);
    });

    gameWrapper.addEventListener('touchmove', (e) => {
        e.preventDefault(); // Prevent scrolling while dragging
        const touch = e.touches[0];
        moveDrag(touch.pageX, touch.pageY);
    });

    gameWrapper.addEventListener('touchend', stopDrag);
    gameWrapper.addEventListener('touchcancel', stopDrag);


    let contextMenu = document.getElementById('context-menu');
    let selectedTile = null;

    document.addEventListener("contextmenu", (event) => event.preventDefault()); // Disable default menu


gridContainer.children.forEach(tile => {
    tile.on("rightdown", (event) => { // 'rightdown' detects right-click in Pixi.js
        event.stopPropagation(); // Prevents event from bubbling up
        event.preventDefault();  // Stops browser menu
        showContextMenu(event.global.x, event.global.y, tile);
    });

    // Long press (Mobile)
    tile.on("pointerdown", (event) => {
        pressTimer = setTimeout(() => {
            showContextMenu(event.global.x, event.global.y, tile);
        }, 500); // Hold for 500ms to trigger
    });

    tile.on("pointerup", () => clearTimeout(pressTimer)); // Cancel if released early
    tile.on("pointerout", () => clearTimeout(pressTimer));

    });


    function showContextMenu(x, y, tile) {
    selectedTile = tile;
    contextMenu.style.display = 'block';
    contextMenu.style.left = x + 'px';
    contextMenu.style.top = y + 'px';
    }

    document.addEventListener("click", () => {
    contextMenu.style.display = "none";
    });

    document.getElementById("edit-tile").addEventListener("click", () => {
    if (selectedTile) {
        selectedTile.tint = Math.random() * 0xffffff; // Example: Change tile color
    }});


document.getElementById("delete-tile").addEventListener("click", () => {
    if (selectedTile) {
        selectedTile.destroy(); // Remove tile
    }});

});





