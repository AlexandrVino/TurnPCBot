


-- Table: public.userinfo

-- DROP TABLE public.userinfo;

CREATE TABLE public.users
(
    chat_id integer NOT NULL,
    language_code character varying(255) COLLATE pg_catalog."default" NOT NULL,
    comps character varying(255) COLLATE pg_catalog."default",
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    CONSTRAINT userinfo_chat_id UNIQUE (chat_id)
)

TABLESPACE pg_default;
ALTER TABLE public.users
    OWNER to postgres;