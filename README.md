# Business-rules-voor-Recommendation-Engine

De code begint met enkele functies, die zorgen voor een connectie met de database en twee functies die queries uitvoeren. Vervolgens zijn er meerdere functies die elk aparte tafels aanmaken voor de nieuwe tabellen.

Voor de collaborative business rule wordt er één nieuwe tabel aangemaakt waar de producten worden getoond die worden aanbevolen. Die producten zijn gefilterd op basis van "views". Dus wat er veel bekeken wordt, word aanbevolen (ze hebben met het gedrag van de website bezoekers te maken!). Daarom is deze tafel gebasseerd op een collaborative rule.

Voor de content business rule zijn er meerdere tafels aangemaakt. Dat is omdat de aanbevelingen in deze regel gebasseerd zijn op doelgroep(elke doelgroep een aparte tafel). Ben je bijvoorbeeld aan het kijken naar een babyproduct, dan krijg je als aanbeveling: "Misschien geinteresseerd in dit product?", waar dan een ander babyproduct verschijnt. (Deze aanbeveling wordt gemaakt d.m.v een filtering onder de doelgroep en de categorie die bekeken wordt). De voorlopige aanbeveling wordt gedaan met behulp van een query, die per doelgroep vijf producten eruit haalt als aanbeveling.

Om de code te testen dient er alleen in de functie "connect()" de eigen gegevens van de postgres database te worden ingevuld.
