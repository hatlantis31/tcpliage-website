# migrations/0002_load_initial_services.py
from django.db import migrations


def load_initial_services(apps, schema_editor):
    Service = apps.get_model('metal_api', 'Service')
    ServiceCharacteristic = apps.get_model(
        'metal_api', 'ServiceCharacteristic')

    services_data = [
        {
            'titre': 'Couvertine',
            'description': 'Fabrication de couvertines sur mesure pour la protection et finition des acrotères',
            'image': '/couvertine/example.jpg',
            'caracteristiques': [
                'Couvertines aluminium',
                'Protection des murs et toitures',
                'Finitions soignées',
                'Sur mesure selon vos dimensions'
            ]
        },
        {
            'titre': 'Habillage',
            'description': 'Solutions d\'habillage métallique pour vos façades et structures',
            'image': '/habillage/example.jpg',
            'caracteristiques': [
                'Habillage de façades',
                'Bardage métallique',
                'Revêtements personnalisés',
                'Différentes finitions disponibles'
            ]
        },
        {
            'titre': 'Matière',
            'description': 'Large gamme de matériaux disponibles pour vos projets',
            'image': '/matiere/example.jpg',
            'caracteristiques': [
                'Aluminium',
                'Acier galvanisé',
                'Acier laqué',
                'Zinc'
            ]
        },
        {
            'titre': 'Quincaillerie',
            'description': 'Fabrication de pièces de quincaillerie sur mesure',
            'image': '/quincaillerie/example.jpg',
            'caracteristiques': [
                'Fixations spéciales',
                'Supports métalliques',
                'Pièces techniques',
                'Accessoires sur mesure'
            ]
        },
        {
            'titre': 'Réalisation',
            'description': 'Réalisation de projets métalliques complexes et sur mesure',
            'image': '/realisation/example.jpg',
            'caracteristiques': [
                'Projets personnalisés',
                'Fabrication précise',
                'Installation possible',
                'Suivi de chantier'
            ]
        },
        {
            'titre': 'Formes Spéciales',
            'description': 'Création de formes métalliques spécifiques selon vos besoins',
            'image': '/shape/example.jpg',
            'caracteristiques': [
                'Pliage complexe',
                'Formes sur mesure',
                'Découpe précise',
                'Solutions adaptées'
            ]
        }
    ]

    for service_data in services_data:
        service = Service.objects.create(
            titre=service_data['titre'],
            description=service_data['description'],
            image=service_data['image']
        )

        for caracteristique in service_data['caracteristiques']:
            ServiceCharacteristic.objects.create(
                service=service,
                description=caracteristique
            )


def reverse_load(apps, schema_editor):
    Service = apps.get_model('metal_api', 'Service')
    Service.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        # Update this to your actual initial migration
        ('metal_api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_services, reverse_load),
    ]
