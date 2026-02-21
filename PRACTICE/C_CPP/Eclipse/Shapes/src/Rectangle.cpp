#include <iostream>
#include "Rectangle.hpp"

Rectangle::Rectangle(Coord2D topLeft, Coord2D bottomDown) : Shape(topLeft) {
	// new Coord2D{ .x = topLeft.x - bottomDown.x, .y = topLeft.y - bottomDown.y }
	dimensions.height = topLeft.x - bottomDown.x;
	dimensions.width = topLeft.y - bottomDown.y;
}

Rectangle::~Rectangle() {
	// TODO Auto-generated destructor stub
}

void Rectangle::resize(double factor) {
	this->resize(factor);
	std::cout << __PRETTY_FUNCTION__ << " " << this << std::endl;
}

void Rectangle::draw() const {
	std::cout << __PRETTY_FUNCTION__ << " " << this << std::endl;
}

bool Rectangle::containsCoordinates(Coord2D coord) const{
	return containsCoordinates(coord);
}

