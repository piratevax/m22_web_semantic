# Projet - M2 BioInfo - Web sémantique

## Contexte générale

On s'intéresse ici à l'extraction de connaissances à partir de données structurées et non structurées. L'application de la méthode retenue se fera sur un corpus de textes en entrée (au format XML pour les données structurées et texte pour les résumés) à partir desquels on souhaite obtenir des associations entre concepts MeSH ou entre termes biomédicaux. Ces associations seront ensuite réutilisées pour constituer une ontologie au format OWL (hiérarchies de concepts, relations, hiérachies de relations, domaines et co-domaines, etc...).

## Constitution du corpus XML

Les fichiers XML devant être traités sont des extractions au format XML MEDLINE de la banque de données des articles scientifiques en santé de la [NLM](https://wwww.ncbi.nlm.nih.gov/pubmed) (National Library of Medcine).

## Fouille de données

À partir de la collection XML, la fouille de données consistera à extraire des règles d'association entre MeSH Descriptor et entre couples (MeSH Descriptor/Qualifier).

## Fouille de textes

L'indexation manuelle de MEDLINE peut être complété par une indexation "automatique". Nous avons utilisé l'[Annotator](https://bioportal.bioontology.org/annotator) de BioPortal.
L'annotator ne fonctionnant que sur des textes de 300 mots, l'indexation automatique portera sur les résumés des notices de MEDLINE (champs Abstract) et les titres.

## Représentation des connaissances

Proposition d'une représentation ontologique des concepts et des ralations.