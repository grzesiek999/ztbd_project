

export default function HomePage() {
    return (
        <div className={'home-page-div-wrapper'}>
            <span>Zaawansowe Techniki Bazodanowe</span>
            <p>Aplikacja służy do porównania, przeprowadzenia analizy i wyznaczenia korzystniejszego systemu bazy danych (relacyjnego lub nierelacyjnego)
                w kotekście aplikacji dla zarządzania urządzeniami użytkowników sterowanych gestami.</p> 
            <p>Wybranymi systemami baz danych zostały: PostgreSQL i MongoDB.</p>
            <p>Aplikacja została zaprojektowana, aby udostępnić użytkownikowi interfejs do wykonywania operacji na bazach danych. 
                Zadaniem aplikacji jest wykonaywanie zapytań API do aplikacji serwer, która wykoanuje operacje CRUD i zwraca czas pracy wybranej operacji CRUD dla każdej próbki, 
                a następnie wyświetla wyniki w postaci tabel, wykresów i średniej arytmetycznej dla każdego systemu zarządzania bazą danych umożliwiając ich porównanie oraz analizę.</p>
            <div className="home-page-images-div">
                <img src="/public/images/postgre-icon.png" alt="postgre image icon error" />
                <img src="/public/images/statistics.png" alt="statistics image icon error" />
                <img src="/public/images/mongodb-icon.png" alt="mongo image icon error" />
            </div>
        </div>
    )
}
