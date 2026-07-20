import 'package:flutter/material.dart';
import '../models/book.dart';
import '../screens/player_screen.dart';
import 'book_card.dart';

class BookSearchDelegate extends SearchDelegate {
  @override
  String get searchFieldLabel => 'Cauta carti sau autori...';

  @override
  List<Widget>? buildActions(BuildContext context) {
    return [
      IconButton(
        icon: const Icon(Icons.clear),
        onPressed: () {
          query = '';
        },
      ),
    ];
  }

  @override
  Widget? buildLeading(BuildContext context) {
    return IconButton(
      icon: const Icon(Icons.arrow_back),
      onPressed: () {
        close(context, null);
      },
    );
  }

  @override
  Widget buildResults(BuildContext context) {
    final results = Book.mockBooks.where((book) {
      final titleLower = book.title.toLowerCase();
      final authorLower = book.author.toLowerCase();
      final searchLower = query.toLowerCase();
      return titleLower.contains(searchLower) || authorLower.contains(searchLower);
    }).toList();

    return _buildBookList(results);
  }

  @override
  Widget buildSuggestions(BuildContext context) {
    final suggestions = Book.mockBooks.where((book) {
      final titleLower = book.title.toLowerCase();
      final authorLower = book.author.toLowerCase();
      final searchLower = query.toLowerCase();
      return titleLower.contains(searchLower) || authorLower.contains(searchLower);
    }).toList();

    return _buildBookList(suggestions);
  }

  Widget _buildBookList(List<Book> books) {
    if (books.isEmpty) {
      return const Center(
        child: Text('Nu am gasit niciun rezultat.'),
      );
    }

    return ListView.builder(
      itemCount: books.length,
      padding: const EdgeInsets.all(16),
      itemBuilder: (context, index) {
        final book = books[index];
        return ListTile(
          leading: ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: Image.network(
              book.imageUrl,
              width: 50,
              height: 50,
              fit: BoxFit.cover,
            ),
          ),
          title: Text(book.title),
          subtitle: Text(book.author),
          onTap: () {
            close(context, null);
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => PlayerScreen(book: book),
              ),
            );
          },
        );
      },
    );
  }
}
