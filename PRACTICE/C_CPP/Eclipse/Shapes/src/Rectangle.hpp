#ifndef RECTANGLE_HPP_
#define RECTANGLE_HPP_

#include "Helper.hpp"
#include "Shape.hpp"

class Rectangle : public Shape {
public:
	Rectangle(Coord2D topLeft, Coord2D bottomDown);
	~Rectangle();
	void resize(double factor);
	void draw() const;
	bool containsCoordinates(Coord2D coord) const;
private:
	Dimensions2D dimensions;
};

#endif /* RECTANGLE_HPP_ */
