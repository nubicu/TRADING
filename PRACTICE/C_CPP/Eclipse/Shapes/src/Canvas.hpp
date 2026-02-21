#ifndef CANVAS_HPP_
#define CANVAS_HPP_

#include <set>
#include "Shape.hpp"

class Canvas {
public :
	void insert(Shape& shape);
	void remove(Shape& shape);
	Shape* shapeAt(Coord2D coord);
	void drawAll();
private :
	std::set<Shape*> myShapes;
};



#endif /* CANVAS_HPP_ */
