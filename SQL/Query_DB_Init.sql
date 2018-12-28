-- ****************** SqlDBM: MySQL ******************;
-- ***************************************************;
USE test;


-- ****************** SqlDBM: MySQL ******************;
-- ***************************************************;

DROP TABLE `Przeglad`;


DROP TABLE `Praca`;


DROP TABLE `Tramwaj`;


DROP TABLE `Motorniczy`;


DROP TABLE `Linia`;



-- ************************************** `Tramwaj`

CREATE TABLE `Tramwaj`
(
 `ID_Tramwaju`       int NOT NULL AUTO_INCREMENT ,
 `Prog_Godzinowy`    int NOT NULL DEFAULT 1000 ,
 `Aktualny_Przebieg` float NOT NULL DEFAULT 0 ,
 `Version`           int NOT NULL DEFAULT 0 ,
PRIMARY KEY (`ID_Tramwaju`)
);






-- ************************************** `Motorniczy`

CREATE TABLE `Motorniczy`
(
 `ID_Motorniczego` int NOT NULL AUTO_INCREMENT ,
 `Imie`            varchar(45) NOT NULL ,
 `Nazwisko`        varchar(45) NOT NULL ,
 `Stawka`          float NOT NULL DEFAULT 12 ,
 `Zatrudniony`     bit NOT NULL DEFAULT 1 ,
 `Version`         int NOT NULL DEFAULT 0 ,
PRIMARY KEY (`ID_Motorniczego`)
);






-- ************************************** `Linia`

CREATE TABLE `Linia`
(
 `ID_Linii`    int NOT NULL AUTO_INCREMENT ,
 `Numer_Linii` int NOT NULL ,
 `Version`     int NOT NULL DEFAULT 0 ,
PRIMARY KEY (`ID_Linii`)
);






-- ************************************** `Przeglad`

CREATE TABLE `Przeglad`
(
 `ID_Przegladu` int NOT NULL AUTO_INCREMENT ,
 `ID_Tramwaju`  int NOT NULL ,
 `Data`         datetime NOT NULL ,
PRIMARY KEY (`ID_Przegladu`),
KEY `fkIdx_57` (`ID_Tramwaju`),
CONSTRAINT `FK_57` FOREIGN KEY `fkIdx_57` (`ID_Tramwaju`) REFERENCES `Tramwaj` (`ID_Tramwaju`)
);






-- ************************************** `Praca`

CREATE TABLE `Praca`
(
 `ID_Pracy`        int NOT NULL AUTO_INCREMENT ,
 `ID_Linii`        int NOT NULL ,
 `ID_Motorniczego` int NOT NULL ,
 `ID_Tramwaju`     int NOT NULL ,
 `PoczatekPracy`   datetime NOT NULL ,
 `KoniecPracy`     datetime ,
 `Wynagrodzenie`   float ,
 `Version`         int NOT NULL DEFAULT 0 ,
PRIMARY KEY (`ID_Pracy`),
KEY `fkIdx_25` (`ID_Linii`),
CONSTRAINT `FK_25` FOREIGN KEY `fkIdx_25` (`ID_Linii`) REFERENCES `Linia` (`ID_Linii`),
KEY `fkIdx_28` (`ID_Motorniczego`),
CONSTRAINT `FK_28` FOREIGN KEY `fkIdx_28` (`ID_Motorniczego`) REFERENCES `Motorniczy` (`ID_Motorniczego`),
KEY `fkIdx_31` (`ID_Tramwaju`),
CONSTRAINT `FK_31` FOREIGN KEY `fkIdx_31` (`ID_Tramwaju`) REFERENCES `Tramwaj` (`ID_Tramwaju`)
);
















-- ****************************************************************
-- ************************* FUNCTIONS ****************************
-- ****************************************************************






-- ************************************** `Obliczanie_Wynagrodzenia`

DROP FUNCTION IF EXISTS Obliczanie_Wynagrodzenia;

DELIMITER //
CREATE FUNCTION Obliczanie_Wynagrodzenia(id_m INT, id_p INT)
   RETURNS float 
 
BEGIN
	DECLARE Poczatek_Pracy datetime; 
	DECLARE Koniec_Pracy datetime; 
	DECLARE Czas_Pracy INT; 
	DECLARE stawka_ float; 
	DECLARE wynik float; 
	SET stawka_ = (SELECT Stawka FROM Motorniczy WHERE ID_Motorniczego = id_m); 
	SET Poczatek_Pracy = (SELECT PoczatekPracy FROM Praca WHERE ID_Pracy= id_p); 
	SET Koniec_Pracy =  (SELECT KoniecPracy FROM Praca WHERE ID_Pracy= id_p); 
	SET wynik = TIMESTAMPDIFF(MINUTE, Poczatek_Pracy, Koniec_Pracy)/60 * stawka_; 
	RETURN wynik; 
END;//

DELIMITER ;






-- ****************************************************************
-- ************************* TRIGGERS *****************************
-- ****************************************************************






-- ************************************** `Licz_Wynagrodzenie`

DROP TRIGGER IF EXISTS Licz_Wynagrodzenie;

DELIMITER //

CREATE TRIGGER Licz_Wynagrodzenie BEFORE update ON Praca
FOR EACH ROW BEGIN
	DECLARE Wynagrodzenie_ float;
    DECLARE Nowy_Przebieg_ float;
    DECLARE Stary_Przebieg_ float;
    DECLARE Stara_wersja_ int;
	DECLARE Nowa_wersja int;

	SET Stara_wersja_ = OLD.version;
	SET Nowa_wersja =  NEW.version;

    IF (Stara_wersja_+1 <> Nowa_wersja) THEN
	SIGNAL sqlstate '45001' set message_text = "Wersje sie nie zgadzaja ";
    END IF; 
	if NEW.KoniecPracy IS NOT NULL THEN
		SELECT Obliczanie_Wynagrodzenia(OLD.ID_Motorniczego, OLD.ID_Pracy) INTO Wynagrodzenie_;
		SET NEW.Wynagrodzenie = Wynagrodzenie_;
	END IF;

    SET Stary_Przebieg_ = (SELECT Aktualny_Przebieg FROM tramwaj WHERE ID_Tramwaju = NEW.ID_Tramwaju);
	SET Nowy_Przebieg_ = TIMESTAMPDIFF(MINUTE, NEW.PoczatekPracy, NEW.KoniecPracy)/60 + Stary_Przebieg_;
	UPDATE tramwaj SET Aktualny_Przebieg = Nowy_Przebieg_ WHERE ID_Tramwaju=1;

END; //

DELIMITER ;


DROP TRIGGER IF EXISTS Licz_Wynagrodzenie2;

DELIMITER //

CREATE TRIGGER Licz_Wynagrodzenie2 BEFORE insert ON Praca
FOR EACH ROW BEGIN
	DECLARE Wynagrodzenie_ float;
    DECLARE Nowy_Przebieg_ float;
    DECLARE Stary_Przebieg_ float;


	if NEW.KoniecPracy IS NOT NULL THEN
		SELECT Obliczanie_Wynagrodzenia(NEW.ID_Motorniczego, NEW.ID_Pracy) INTO Wynagrodzenie_;
		SET NEW.Wynagrodzenie = Wynagrodzenie_;
	END IF;

    SET Stary_Przebieg_ = (SELECT Aktualny_Przebieg FROM tramwaj WHERE ID_Tramwaju = NEW.ID_Tramwaju);
	SET Nowy_Przebieg_ = TIMESTAMPDIFF(MINUTE, NEW.PoczatekPracy, NEW.KoniecPracy)/60 + Stary_Przebieg_;
	UPDATE tramwaj SET Aktualny_Przebieg = Nowy_Przebieg_ WHERE ID_Tramwaju=1;

END; //

DELIMITER ;



-- ************************************** `Stan_Przebiegu`

DROP TRIGGER IF EXISTS Stan_Przebiegu;

DELIMITER //

CREATE TRIGGER Stan_Przebiegu AFTER insert ON Praca
FOR EACH ROW BEGIN

DECLARE Aktualny_Przebieg_ float;
DECLARE Prog_Godzinowy_ int;
DECLARE Zatrudniony_ bit;

SET Aktualny_Przebieg_ = (SELECT Aktualny_Przebieg FROM Tramwaj WHERE ID_Tramwaju=NEW.ID_Tramwaju);
SET Prog_Godzinowy_ = (SELECT Prog_Godzinowy FROM Tramwaj WHERE ID_Tramwaju=NEW.ID_Tramwaju);
SET Zatrudniony_ = (SELECT Zatrudniony FROM Motorniczy WHERE ID_Motorniczego=NEW.ID_Motorniczego);

    IF (Zatrudniony_ <> 1) THEN
	SIGNAL sqlstate '45001' set message_text = "Dodawany motorniczy nie jest juz zatrudniony!";
    END IF; 
    
    IF (Aktualny_Przebieg_ > Prog_Godzinowy_) THEN
	SIGNAL sqlstate '45001' set message_text = "Przebieg pojazdu zbyt wysoki! Weź go na warsztat";
    END IF; 
    


END; //

DELIMITER ;

-- ************************************** `Sprawdz_wersje`



DELIMITER ;