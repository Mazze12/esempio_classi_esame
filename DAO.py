from database.DB_connect import DBConnect
from model.arco import Arco
from model.artista import Artista
from model.genere import Genere


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGeneri():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary = True)
        result = []

        query = """select * from genre g"""
        cursor.execute(query)
        for row in cursor:
            result.append(Genere(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArtisti():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []

        query = """select * 
                   from artist a"""
        cursor.execute(query)
        for row in cursor:
            result.append(Artista(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(genere):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []

        query = """ select a.*
                    from artist a
                    join album al on a.ArtistId = al.ArtistId
                    join track t on al.AlbumId = t.AlbumId
                    where t.genreId = %s
                    group by a.ArtistId"""
        cursor.execute(query, (genere.GenreId,))
        for row in cursor:
            result.append(Artista(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(genere, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []

        query = """ WITH ArtistiDelGenere AS (
                    -- 1. Seleziono gli artisti che possiedono almeno un brano
                    -- appartenente al genere scelto. Questi saranno i vertici del grafo.
                    SELECT DISTINCT al.ArtistId
                    FROM track t
                    JOIN album al  ON t.AlbumId = al.AlbumId
                    WHERE t.GenreId = %s
                    ),
    
    PopolaritaTotaleArtisti AS (
                    -- 2. Calcolo la popolarità totale di ogni artista.
                    -- La popolarità è la somma di tutti i brani acquistati di quell'artista.
                    SELECT al.ArtistId, SUM(il.Quantity) AS Popolarita
                    FROM invoiceline il
                    JOIN track t ON il.TrackId = t.TrackId
                    JOIN album al ON t.AlbumId = al.AlbumId
                    WHERE t.GenreId = %s
                    GROUP BY al.ArtistId
                    ),
    
     ClientiArtisti AS (
                        -- 3. Individuo quali clienti hanno acquistato almeno
                        -- un brano di ciascun artista.
                        --
                        -- Uso DISTINCT perché in questa fase mi interessa solo sapere
                        -- se un cliente ha acquistato almeno un brano di un artista, non quante volte.
                        SELECT DISTINCT i.CustomerId, al.ArtistId
                        FROM invoice i
                        JOIN invoiceline il ON i.InvoiceId = il.InvoiceId
                        JOIN track t ON il.TrackId = t.TrackId
                        JOIN album al ON t.AlbumId = al.AlbumId
                        WHERE t.GenreId = %s
                    ),
                    
     ArchiPop AS (
                    -- 4. Creo le coppie di artisti che hanno almeno un cliente in
                    --  comune e associo subito la popolarità totale di ciascun artista.
                    SELECT DISTINCT A.ArtistId AS ArtistaA, pA.Popolarita AS PopA, B.ArtistId AS ArtistaB, pB.Popolarita AS PopB
                    FROM ClientiArtisti A
                    JOIN ClientiArtisti B ON A.CustomerId = B.CustomerId AND A.ArtistId < B.ArtistId
                    -- Associo la popolarità totale dell'artista A
                    JOIN PopolaritaTotaleArtisti pA ON A.ArtistId = pA.ArtistId
                    -- Associo la popolarità totale dell'artista B
                    JOIN PopolaritaTotaleArtisti pB ON B.ArtistId = pB.ArtistId
                    -- Tengo solo gli artisti che appartengono al genere selezionato,
                    -- cioè i vertici effettivi del grafo.
                    WHERE A.ArtistId IN (   SELECT ArtistId
                                            FROM ArtistiDelGenere
                                        )
                    AND B.ArtistId IN (   SELECT ArtistId
                                            FROM ArtistiDelGenere
                                        )
                    )
#6. 
#1. ArtistaA è più popolare di ArtistaB.              
SELECT ArtistaA AS NodoSorgente, ArtistaB AS NodoDestinazione, PopA + PopB AS PesoArco
FROM ArchiPop
WHERE PopA > PopB

UNION ALL
                
#2. ArtistaB è più popolare di ArtistaA
SELECT ArtistaB AS NodoSorgente, ArtistaA AS NodoDestinazione, PopA + PopB AS PesoArco
FROM ArchiPop
WHERE PopB > PopA
                
UNION ALL

#3. le popolarità sono uguali
SELECT
ArtistaA AS NodoSorgente,
ArtistaB AS NodoDestinazione,
PopA + PopB AS PesoArco
FROM ArchiPop
WHERE PopA = PopB
                
UNION ALL
                
#4. le popolarità sono uguali
SELECT ArtistaB AS NodoSorgente, ArtistaA AS NodoDestinazione, PopA + PopB AS PesoArco
FROM ArchiPop
WHERE PopA = PopB;"""
        cursor.execute(query, (genere.GenreId, genere.GenreId, genere.GenreId,))
        i = 0
        for row in cursor:
            i+=1
            result.append(Arco(1, idMap[row["NodoSorgente"]], idMap[row["NodoDestinazione"]], row["PesoArco"]))

        cursor.close()
        conn.close()
        return result





