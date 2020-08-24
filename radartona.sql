--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4 (Debian 12.4-1)
-- Dumped by pg_dump version 12.4 (Debian 12.4-1)

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

SET default_table_access_method = heap;

--
-- Name: contagens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contagens (
    id integer NOT NULL,
    localidade integer,
    faixa integer,
    tipo integer,
    contagem integer,
    autuacoes integer,
    placas integer,
    data_e_hora timestamp with time zone
);


ALTER TABLE public.contagens OWNER TO postgres;

--
-- Name: contagens_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contagens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contagens_id_seq OWNER TO postgres;

--
-- Name: contagens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contagens_id_seq OWNED BY public.contagens.id;


--
-- Name: trajetos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.trajetos (
    id integer NOT NULL,
    tipo integer,
    data_inicio timestamp with time zone,
    data_final timestamp with time zone,
    origem integer,
    destino integer,
    v0 integer,
    v1 integer
);


ALTER TABLE public.trajetos OWNER TO postgres;

--
-- Name: trajetos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.trajetos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trajetos_id_seq OWNER TO postgres;

--
-- Name: trajetos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.trajetos_id_seq OWNED BY public.trajetos.id;


--
-- Name: viagens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.viagens (
    id integer NOT NULL,
    inicio integer,
    data_inicio timestamp with time zone,
    final integer,
    data_final timestamp with time zone
);


ALTER TABLE public.viagens OWNER TO postgres;

--
-- Name: viagens_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.viagens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.viagens_id_seq OWNER TO postgres;

--
-- Name: viagens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.viagens_id_seq OWNED BY public.viagens.id;


--
-- Name: contagens id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contagens ALTER COLUMN id SET DEFAULT nextval('public.contagens_id_seq'::regclass);


--
-- Name: trajetos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trajetos ALTER COLUMN id SET DEFAULT nextval('public.trajetos_id_seq'::regclass);


--
-- Name: viagens id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.viagens ALTER COLUMN id SET DEFAULT nextval('public.viagens_id_seq'::regclass);


--
-- Data for Name: contagens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contagens (id, localidade, faixa, tipo, contagem, autuacoes, placas, data_e_hora) FROM stdin;
\.


--
-- Data for Name: trajetos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.trajetos (id, tipo, data_inicio, data_final, origem, destino, v0, v1) FROM stdin;
\.


--
-- Data for Name: viagens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.viagens (id, inicio, data_inicio, final, data_final) FROM stdin;
\.


--
-- Name: contagens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contagens_id_seq', 1, false);


--
-- Name: trajetos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.trajetos_id_seq', 1, false);


--
-- Name: viagens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.viagens_id_seq', 1, false);


--
-- Name: contagens contagens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contagens
    ADD CONSTRAINT contagens_pkey PRIMARY KEY (id);


--
-- Name: trajetos trajetos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trajetos
    ADD CONSTRAINT trajetos_pkey PRIMARY KEY (id);


--
-- Name: viagens viagens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.viagens
    ADD CONSTRAINT viagens_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

