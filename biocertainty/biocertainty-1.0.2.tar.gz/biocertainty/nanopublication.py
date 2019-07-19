#-*- coding: utf-8 -*-
#!/usr/bin/env python

from .certainty import Certainty
from .seeker import doi_pmc_seeker
import re
import md5
import uuid
import datetime


RE = '(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)'


def Nanopublication(pmc_doi, CLAIM):
    categorization = Certainty(CLAIM)
    doi = doi_pmc_seeker(pmc_doi)
    index = str(uuid.uuid1()) 
    try:
        if bool(re.match(RE, doi)) == True:
            text = ("https://dx.doi.org/%s") % (doi)
            nanopub = ("""@prefix this: <http://linkeddata.systems/nanopubs_mario/CertID_{0}> .
@prefix sub: <http://linkeddata.systems/nanopubs_mario/CertID_{0}#> .
@prefix void: <http://rdfs.org/ns/void#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dcelem: <http://purl.org/dc/elements/1.1/> .
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix sio: <http://semanticscience.org/resource/> .
@prefix pav: <http://swan.mindinformatics.org/ontologies/1.2/pav/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix swande: <http://purl.org/swan/1.2/discourse-elements/> .
@prefix swanco: <http://purl.org/swan/1.2/swan-commons/> .
@prefix schema: <https://schema.org/> .
@prefix orca: <http://vocab.deri.ie/orca#/> .
@prefix doi: <http://dx.doi.org/> .
@prefix text: <https://dx.doi.org/{1}#> .
@prefix swanqual: <http://swan.mindinformatics.org/ontologies/1.2/rsqualifiers/> .
@prefix certainty: <http://w3id.org/orca-x#> .

sub:Head {6}
        this: np:hasAssertion sub:assertion ;
        np:hasProvenance sub:provenance ;
        np:hasPublicationInfo sub:pubinfo ;
        a np:Nanopublication .
{7}

sub:assertion {6}
        <https://dx.doi.org/{1}/#{2}> sio:has-value 'CertID_{0}'@en' .
        <https://dx.doi.org/{1}/#{2}> certainty:hasConfidenceLevel '{3}'@en .
{7}

sub:provenance {6}   
        sub:assertion dcterms:author "Certainty Classifier" ;
        dcterms:title "Automated Certainty Classification of Statement from https:dx.doi.org/{1}" ;
        dcat:distribution sub:_1 ;
        prov:wasGeneratedBy "Mario Prieto's Certainty Classifier" ;
        certainty:hasConfidenceLevel  certainty:{3} .

        sub:_1   dcelem:format "application/pdf" ;
        a void:Dataset , dcat:Distribution ;
        schema:identifier '{1}' ;
        dcat:downloadURL <{4}> .

{7}

sub:pubinfo {6}
        this: dcterms:created '{5}'^^xsd:dateTime ;
        dcterms:rights <https://creativecommons.org/publicdomain/zero/1.0> ;
        dcterms:rightsHolder <https://orcid.org/0000-0002-9416-6743> ;
        pav:authoredBy "Mario Prieto" , <https://orcid.org/0000-0002-9416-6743> ;
        pav:versionNumber "1" .
{7}
    """).format(index, doi, md5.new(CLAIM).hexdigest(), categorization, text, datetime.date.today(), '{', '}')
            return nanopub, index
        else:
            text = ("https://www.ebi.ac.uk/europepmc/webservices/rest/%s/fullTextXML") % (pmc)
            nanopub = ("""@prefix this: <http://linkeddata.systems/nanopubs_mario/CertID_{0}> .
@prefix sub: <http://linkeddata.systems/nanopubs_mario/CertID_{0}#> .
@prefix void: <http://rdfs.org/ns/void#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dcelem: <http://purl.org/dc/elements/1.1/> .
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix sio: <http://semanticscience.org/resource/> .
@prefix pav: <http://swan.mindinformatics.org/ontologies/1.2/pav/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix swande: <http://purl.org/swan/1.2/discourse-elements/> .
@prefix swanco: <http://purl.org/swan/1.2/swan-commons/> .
@prefix schema: <https://schema.org/> .
@prefix orca: <http://vocab.deri.ie/orca#/> .
@prefix swanqual: <http://swan.mindinformatics.org/ontologies/1.2/rsqualifiers/> .
@prefix text: <https://www.ebi.ac.uk/europepmc/webservices/rest/{1}/fullTextXML#> .
@prefix certainty: <http://w3id.org/orca-x#> .

sub:Head {6}
        this: np:hasAssertion sub:assertion ;
        np:hasProvenance sub:provenance ;
        np:hasPublicationInfo sub:pubinfo ;
        a np:Nanopublication .
{7}

sub:assertion {6}
        <https://www.ebi.ac.uk/europepmc/webservices/rest/{1}/fullTextXML/#{2}> sio:has-value 'CertID_{0}'@en' .
        <https://www.ebi.ac.uk/europepmc/webservices/rest/{1}/fullTextXML/#{2}> certainty:hasConfidenceLevel '{3}'@en .
{7}

sub:provenance {6}   
        sub:assertion dcterms:author "Certainty Classifier" ;
        dcterms:title "Automated Certainty Classification of Statement from {6}4}" ;
        dcat:distribution sub:_1 ;
        prov:wasGeneratedBy "Mario Prieto's Certainty Classifier" ;
        certainty:hasConfidenceLevel  certainty:{3} .

        sub:_1   dcelem:format "application/pdf" ;
        a void:Dataset , dcat:Distribution ;
        schema:identifier '{1}' ;
        dcat:downloadURL <{4}> .

{7}

sub:pubinfo {6}
        this: dcterms:created '{5}'^^xsd:dateTime ;
        dcterms:rights <https://creativecommons.org/publicdomain/zero/1.0> ;
        dcterms:rightsHolder <https://orcid.org/0000-0002-9416-6743> ;
        pav:authoredBy "Mario Prieto" , <https://orcid.org/0000-0002-9416-6743> ;
        pav:versionNumber "1" .
{7}
    """).format(index, pmc, md5.new(CLAIM).hexdigest(), categorization, text, datetime.date.today(), '{', '}')
            return nanopub, index

    except AssertionError as error:
        print(error)