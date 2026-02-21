#include <iostream>
#include <algorithm>
#include "Canvas.hpp"
#include "Circle.hpp"
#include "Rectangle.hpp"

void Canvas::insert(Shape& shape) {
	myShapes.insert(&shape);
}

void Canvas::remove(Shape& shape) {
		myShapes.erase(&shape);
}

Shape* Canvas::shapeAt(Coord2D coord) {
	for (auto shape : myShapes) {
		if(shape->containsCoordinates(coord)) {
			return shape;
		}
	}
	return nullptr;
}

void Canvas::drawAll() {
	for (auto shape : myShapes) {
		shape->draw();
	}
}

int main() {
	Canvas canvas;

	Coord2D coord1 = {12, 15}, coord2 = {22, 25}, coord3 = {32, 35};
	Circle c1(coord1, 3), c2(coord2, 5), c3(coord3, 4);
	Coord2D coord11 = {0,0}, coord12 = {20,20}, coord13 = {40,40};
	Coord2D coord21 = {20,30}, coord22 = {40,50}, coord23 = {60,60};
	Rectangle r1(coord11, coord21), r2(coord12, coord22), r3(coord13, coord23);

	canvas.insert(c1);
	canvas.insert(r1);
	canvas.insert(c2);
	canvas.insert(c3);
	canvas.insert(r3);
	canvas.insert(r2);

	canvas.drawAll();

	std::cout << "Perform removal operations" <<std::endl;

	canvas.remove(r3);
	canvas.remove(r1);

	canvas.drawAll();

	std::cout << std::endl << "Execution terminated successfully!" << std::endl;
	return 0;
}
