--
-- PostgreSQL database dump
--

-- Dumped from database version 11.16 (Debian 11.16-1.pgdg90+1)
-- Dumped by pg_dump version 11.16 (Debian 11.16-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: articolo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.articolo (
	codice character varying(255) NOT NULL,
	descrizione character varying(255) NOT NULL,
	unita_misura character varying(255),
	soluzione character varying(255),
	codice_tipologia character varying(255),
	tipologia character varying(255),
	famiglia character varying(255),
	diametro numeric,
	rapporto_k numeric,
	rinforzato boolean
);


ALTER TABLE public.articolo OWNER TO postgres;

--
-- Name: articolo_in_fattura; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.articolo_in_fattura (
	codice_articolo_fk character varying(255) NOT NULL,
	codice_fattura_fk character varying(255) NOT NULL,
	quantita numeric NOT NULL,
	data_fattura_fk date NOT NULL,
	descrizione_articolo_fk character varying(255) NOT NULL,
	prezzo numeric NOT NULL
);


ALTER TABLE public.articolo_in_fattura OWNER TO postgres;

--
-- Name: cliente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cliente (
	codice_bms integer NOT NULL,
	ragione_sociale character varying(255),
	alias character varying(255) DEFAULT NULL::character varying,
	commerciale character varying(255),
	classificazione character varying(255),
	settore character varying(255),
	sottosettore character varying(255),
	dettaglio character varying(255) DEFAULT NULL::character varying,
	tipologia_federtec character varying(255),
	paesi character varying(255),
	continente character varying(255),
	regione character varying(255),
	provincia character varying(255)
);


ALTER TABLE public.cliente OWNER TO postgres;

--
-- Name: fattura; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fattura (
	codice character varying(255) NOT NULL,
	data date NOT NULL,
	registro_iva character varying(255),
	cliente_fk integer NOT NULL
);


ALTER TABLE public.fattura OWNER TO postgres;

--
-- Name: test; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.test (
	id integer
);


ALTER TABLE public.test OWNER TO postgres;

--
-- Name: articolo_in_fattura articolo_in_fattura_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.articolo_in_fattura
	ADD CONSTRAINT articolo_in_fattura_pkey PRIMARY KEY (codice_articolo_fk, codice_fattura_fk, quantita, data_fattura_fk, descrizione_articolo_fk, prezzo);


--
-- Name: articolo articolo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.articolo
	ADD CONSTRAINT articolo_pkey PRIMARY KEY (codice, descrizione);


--
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
	ADD CONSTRAINT cliente_pkey PRIMARY KEY (codice_bms);


--
-- Name: fattura fattura_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fattura
	ADD CONSTRAINT fattura_pkey PRIMARY KEY (codice, data);


--
-- Name: articolo_in_fattura articolo_in_fattura_codice_articolo_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.articolo_in_fattura
	ADD CONSTRAINT articolo_in_fattura_codice_articolo_fk_fkey FOREIGN KEY (codice_articolo_fk, descrizione_articolo_fk) REFERENCES public.articolo(codice, descrizione);


--
-- Name: articolo_in_fattura articolo_in_fattura_codice_fattura_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.articolo_in_fattura
	ADD CONSTRAINT articolo_in_fattura_codice_fattura_fk_fkey FOREIGN KEY (codice_fattura_fk, data_fattura_fk) REFERENCES public.fattura(codice, data);


--
-- Name: fattura fattura_cliente_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fattura
	ADD CONSTRAINT fattura_cliente_fk_fkey FOREIGN KEY (cliente_fk) REFERENCES public.cliente(codice_bms);


--
-- PostgreSQL database dump complete
--