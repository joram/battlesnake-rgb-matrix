void board_0(RGBmatrixPanel matrix){
	matrix.fillRect(0, 0, 32, 32, matrix.Color333(0, 7, 0));
	matrix.fillRect(6, 6, 20, 20, matrix.Color333(0, 0, 0));

	// snake 1
	matrix.drawPixel(11, 11, matrix.Color333(7, 0, 0));
	matrix.drawPixel(11, 12, matrix.Color333(7, 0, 0));

	// snake 2
	matrix.drawPixel(24, 11, matrix.Color333(7, 0, 0));
	matrix.drawPixel(24, 12, matrix.Color333(7, 0, 0));

	// Food
	matrix.drawPixel(6, 6, matrix.Color333(2, 2, 2));
	matrix.drawPixel(25, 25, matrix.Color333(2, 2, 2));
}