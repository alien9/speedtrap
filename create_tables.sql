create table contagens (id serial not null, localidade integer,
 faixa integer,
 tipo  integer, contagem integer,
 autuacoes integer,
 placas integer,
 data_e_hora timestamp with time zone, PRIMARY KEY(id));
 
 
create table viagens (
 id serial not null,
 inicio  integer,
 data_inicio  timestamp with time zone,
 final  integer,
 data_final  timestamp with time zone,
 tipo integer, primary key(id));


create table trajetos (
 id serial not null,
 tipo  integer,
 data_inicio  timestamp without time zone,
 data_final  timestamp without time zone,
 origem  integer,
 destino  integer,
 viagem  integer,
 v0  integer,
 v1  integer, primary key(id));
