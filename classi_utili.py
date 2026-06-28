#Classe Arco
from dataclasses import dataclass


@dataclass
class Arco:
   id: int
   nodoSorgente:
   nodoDestinazione:
   pesoArco: int


   def __hash__(self):
       return hash(self.id)


   def __eq__(self,other):
       return self.id == other.id


   def __str__(self):
       return f"{self.nodoSorgente.name} --> {self.nodoDestinazione.name}: {self.pesoArco}"
   




#Classi utili database Chinook
#Classe Album
from dataclasses import dataclass


@dataclass
class Album:
   AlbumId: int
   Title: str
   ArtistId:int


   def __hash__(self):
       return hash(self.AlbumId)


   def __eq__(self, other):
       return self.AlbumId == other.AlbumId


   def __str__(self):
       return f"({self.AlbumId}) {self.Title}"


#Classe Artista
from dataclasses import dataclass




@dataclass
class Artista:
   ArtistId:int
   Name:str


   def __hash__(self):
       return hash(self.ArtistId)


   def __eq__(self, other):
       return self.ArtistId == other.ArtistId


   def __str__(self):
       return f"({self.ArtistId}) {self.Name}"

#Classe Customer
from dataclasses import dataclass




@dataclass
class Customer:
   CustomerId:int
   FirstName:str
   LastName:str
   Company:str
   Address:str
   City:str
   State:str
   Country:str
   PostalCode:str
   Phone:str
   Fax:str
   Email:str
   SupportRepId:int


   def __hash__(self):
       return hash(self.CustomerId)


   def __eq__(self, other):
       return self.CustomerId == other.CustomerId


   def __str__(self):
       return f"({self.CustomerId}) {self.FirstName} {self.LastName}"

Classe Employee
from dataclasses import dataclass
from datetime import date




#@dataclass
class Employee:
   EmployeeId: int
   LastName: str
   FirstName: str
   Title: str
   ReportsTo: int
   BirthDate: date
   HireDate: date
   Address:str
   City:str
   State:str
   Country:str
   PostalCode:str
   Phone:str
   Fax:str
   Email:str


   def __hash__(self):
       return hash(self.EmployeeId)


   def __eq__(self, other):
       return self.EmployeeId == other.EmployeeId


   def __str__(self):
       return f"({self.EmployeeId}) {self.LastName} {self.FirstName}"

#Classe Genere
from dataclasses import dataclass




@dataclass
class Genere:
   GenreId: int
   Name: str


   def __hash__(self):
       return hash(self.GenreId)


   def __eq__(self, other):
       return self.GenreId == other.GenereId


   def __str__(self):
       return f"({self.GenreId}) {self.Name}"

#Classe Invoice
import datetime
from dataclasses import dataclass




@dataclass
class Invoice:
   InvoiceId:int
   CustomerId:int
   InvoiceDate: datetime.date
   BillingAddress:str
   BillingCity:str
   BillingState:str
   BillingCountry:str
   BillingPostalCode:str
   Total:int


   def __hash__(self):
       return hash(self.InvoiceId)


   def __eq__(self, other):
       return self.InvoiceId== other.InvoiceId


   def __str__(self):
       return f"({self.InvoiceId}) {self.Total}"

#Classe mediaType
from dataclasses import dataclass




@dataclass
class MediaType:
   MediaTypeId: int
   Name: str


   def __hash__(self):
       return hash(self.MediaTypeId)


   def __eq__(self, other):
       return self.MediaTypeId == other.MediaTypeId


   def __str__(self):
       return f"({self.MediaTypeId}) {self.Name}"

#Classe playList
from dataclasses import dataclass




@dataclass
class PlayList:
   PlaylistId:int
   Name: str




   def __hash__(self):
       return hash(self.PlaylistId)


   def __eq__(self, other):
       return self.PlaylistId == other.PlaylistId


   def __str__(self):
       return f"({self.PlaylistId}) {self.Name}"

#Classe Traccia
from dataclasses import dataclass




@dataclass
class Traccia:
   TrackId: int
   Name:str
   AlbumId:int
   MediaTypeId: int
   GenreId: int
   Composer: str
   Milliseconds: int
   Bytes: int
   UnitPrice: int


   def __hash__(self):
       return hash(self.TrackId)


   def __eq__(self, other):
       return self.TrackId == other.TrackId


   def __str__(self):
       return f"({self.TrackId}) {self.Name}"
