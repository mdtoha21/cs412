
from django.db import models
from datetime import datetime
# Create your models here.





class Voter(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10, blank=True, null=True)
    street_name = models.CharField(max_length=200)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2, blank=True, null=True)
    precinct_number = models.CharField(max_length=10)

    # Elections (store as booleans)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    voter_score = models.IntegerField(default=0)

    def __str__(self):
        return (f"{self.first_name} {self.last_name} ({self.party_affiliation}) | "
            f"{self.street_number} {self.street_name}, Apt {self.apartment_number}, "
            f"{self.zip_code} | DOB: {self.date_of_birth} | Score: {self.voter_score}")

def load_data():
    filename = '/Users/mdtoha/Desktop/newton_voters.csv'
    f = open(filename)
    f.readline()  # discard header

    for line in f:
        fields = [f.strip() for f in line.split(',')]
        
        try:
            voter = Voter(
                last_name=fields[1],
                first_name=fields[2],
                street_number=fields[3] or None,
                street_name=fields[4],
                apartment_number=fields[5] or None,
                zip_code=fields[6],
                date_of_birth=datetime.strptime(fields[7], "%Y-%m-%d").date(),
                date_of_registration=datetime.strptime(fields[8], "%Y-%m-%d").date(),
                party_affiliation=fields[9] or None,
                precinct_number=fields[10],
                v20state=fields[11].upper() == "TRUE",
                v21town=fields[12].upper() == "TRUE",
                v21primary=fields[13].upper() == "TRUE",
                v22general=fields[14].upper() == "TRUE",
                v23town=fields[15].upper() == "TRUE",
                voter_score=int(fields[16])
            )
            voter.save()
            print(f'Created voter: {voter}')
            
        except Exception as e:
            print(f"Skipped: {fields}, reason: {e}")

    print(f'Done. Created {len(Voter.objects.all())} voters.')