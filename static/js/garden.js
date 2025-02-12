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
            tile.on("pointerdown", () => {
                tile.tint = Math.random() * 0xffffff; // Change color on click
            });

            // Add the tile to the grid container
            gridContainer.addChild(tile);
        }
    }

    // Implement drag functionality
    let isDragging = false;
    let lastX = 0, lastY = 0;

    const wrapperWidth = gameWrapper.offsetWidth;
    const wrapperHeight = gameWrapper.offsetHeight;
    const containerWidth = gameContainer.offsetWidth;
    const containerHeight = gameContainer.offsetHeight;

    // Mouse down event to start dragging

    gameWrapper.addEventListener('mousedown', (e) => {
        isDragging = true;
        lastX = e.pageX;
        lastY = e.pageY;
        gameWrapper.style.cursor = 'grabbing'; // Change cursor when dragging starts
    });

    // Mouse move event to move the canvas within the wrapper
    gameWrapper.addEventListener('mousemove', (e) => {
        if (isDragging) {
            const dx = e.pageX - lastX;
            const dy = e.pageY - lastY;

            // Calculate the new position of the game container (canvas)
            let newLeft = gameContainer.offsetLeft + dx;
            let newTop = gameContainer.offsetTop + dy;

            // Ensure the canvas doesn't move beyond the left and right boundaries
            if (newLeft > 0) newLeft = 0;  // Prevent moving too far to the right
            if (newLeft < wrapperWidth - containerWidth) newLeft = wrapperWidth - containerWidth; // Prevent moving too far to the left

            // Ensure the canvas doesn't move beyond the top and bottom boundaries
            if (newTop > 0) newTop = 0;  // Prevent moving too far down
            if (newTop < wrapperHeight - containerHeight) newTop = wrapperHeight - containerHeight; // Prevent moving too far up

            // Apply the calculated position to the canvas
            gameContainer.style.left = newLeft + 'px';
            gameContainer.style.top = newTop + 'px';

            // Update last positions for the next move event
            lastX = e.pageX;
            lastY = e.pageY;
        }
    });

    // Mouse up event to stop dragging
    gameWrapper.addEventListener('mouseup', () => {
        isDragging = false;
        gameWrapper.style.cursor = 'grab'; // Reset cursor when dragging stops
    });

    gameWrapper.addEventListener('mouseleave', () => {
        isDragging = false;
        gameWrapper.style.cursor = 'grab'; // Reset cursor
    });
});
