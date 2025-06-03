#!/usr/bin/env python3
"""
Script d'initialisation de la base de données
Usage: python init_db.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Code

def init_database():
    """Initialise la base de données"""
    with app.app_context():
        print("🗃️  Création des tables...")
        
        # Supprimer toutes les tables (attention en production !)
        # db.drop_all()
        
        # Créer toutes les tables
        db.create_all()
        
        print("✅ Tables créées avec succès!")
        
        # Optionnel : Insérer des données de test
        if os.getenv('FLASK_ENV') != 'production':
            print("📊 Insertion de données de test...")
            test_user = User(
                phone="+221771234567",
                first_name="Test",
                last_name="User"
            )
            db.session.add(test_user)
            db.session.commit()
            print("✅ Données de test ajoutées!")

def check_database():
    """Vérifie l'état de la base de données"""
    with app.app_context():
        try:
            # Test de connexion
            db.session.execute('SELECT 1')
            print("✅ Connexion à la base de données OK")
            
            # Compter les utilisateurs
            user_count = User.query.count()
            code_count = Code.query.count()
            
            print(f"📊 Statistiques:")
            print(f"   - Utilisateurs: {user_count}")
            print(f"   - Codes: {code_count}")
            
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            return False
    return True

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Gestionnaire de base de données')
    parser.add_argument('--init', action='store_true', help='Initialiser la DB')
    parser.add_argument('--check', action='store_true', help='Vérifier la DB')
    
    args = parser.parse_args()
    
    if args.init:
        init_database()
    elif args.check:
        check_database()
    else:
        print("Usage: python init_db.py --init ou --check")