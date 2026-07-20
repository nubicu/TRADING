class Book {
  final String id;
  final String title;
  final String author;
  final String imageUrl;
  final String audioUrl;
  final String summary;
  final Duration duration;
  final String category;

  Book({
    required this.id,
    required this.title,
    required this.author,
    required this.imageUrl,
    required this.audioUrl,
    required this.summary,
    required this.duration,
    required this.category,
  });

  // Date de exemplu (Mock Data)
  static List<Book> mockBooks = [
    Book(
      id: '1',
      title: 'Sapiens: Scurta istorie a omenirii',
      author: 'Yuval Noah Harari',
      imageUrl: 'https://m.media-amazon.com/images/I/41-S6Y6V5CL._SL500_.jpg',
      audioUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3', // Exemplu audio
      summary: 'Sapiens exploreaza modul in care specia noastra a ajuns sa domine planeta, de la revolutia cognitiva la cea industriala.',
      duration: const Duration(minutes: 15, seconds: 45),
      category: 'Istorie',
    ),
    Book(
      id: '2',
      title: 'Atomic Habits',
      author: 'James Clear',
      imageUrl: 'https://m.media-amazon.com/images/I/513Y5o-DYtL._SL500_.jpg',
      audioUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3',
      summary: 'O metoda usoara si dovedita de a-ti construi obiceiuri bune si de a scapa de cele rele.',
      duration: const Duration(minutes: 14, seconds: 20),
      category: 'Dezvoltare Personala',
    ),
    Book(
      id: '3',
      title: 'Tata Bogat, Tata Sarac',
      author: 'Robert Kiyosaki',
      imageUrl: 'https://m.media-amazon.com/images/I/51H78D-5AUL._SL500_.jpg',
      audioUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3',
      summary: 'Lectii despre bani pe care parintii bogati le transmit copiilor lor, dar cei saraci nu le fac.',
      duration: const Duration(minutes: 16, seconds: 10),
      category: 'Educatie Financiara',
    ),
  ];
}
