# ruff: noqa: E501

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ArticleSection:
    title: str
    paragraphs: tuple[str, ...]
    bullets: tuple[str, ...] = ()


@dataclass(frozen=True)
class BlogArticle:
    slug: str
    title: str
    summary: str
    published_at: str
    read_time: str
    categories: tuple[str, ...]
    hero_image: str
    eyebrow: str
    hero_note: str
    intro: str
    takeaways: tuple[str, ...]
    sections: tuple[ArticleSection, ...]


BLOG_ARTICLES: tuple[BlogArticle, ...] = (
    BlogArticle(
        slug="estructurar-api-net-saas",
        title="Cómo estructurar una API .NET para un SaaS sin perder mantenibilidad",
        summary=(
            "Una guía práctica para separar dominio, aplicación e infraestructura "
            "sin convertir la arquitectura en teoría vacía."
        ),
        published_at="12 Nov 2025",
        read_time="5 min",
        categories=("Backend", ".NET", "Arquitectura"),
        hero_image=(
            "https://images.unsplash.com/photo-1555066931-4365d14bab8c"
            "?w=1200&h=720&fit=crop"
        ),
        eyebrow="Clean architecture aplicada",
        hero_note="Pensado para equipos que necesitan crecer sin rehacer todo cada trimestre.",
        intro=(
            "Cuando una API arranca bien, el equipo entrega rápido. Cuando arranca "
            "mal, cada feature nueva te cobra intereses. La diferencia no está en "
            "usar más capas por deporte, sino en entender qué responsabilidad vive "
            "en cada lugar."
        ),
        takeaways=(
            "El dominio no debería conocer frameworks, HTTP ni bases de datos.",
            "La capa de aplicación orquesta casos de uso, no reglas de negocio profundas.",
            "La infraestructura entra última, como detalle reemplazable y testeable.",
        ),
        sections=(
            ArticleSection(
                title="1. Empezá por los límites, no por los controladores",
                paragraphs=(
                    "El error clásico es arrancar desde el framework y dejar que la "
                    "estructura del proyecto copie la estructura de ASP.NET. Eso te da "
                    "velocidad inicial, pero también acopla cada decisión futura al "
                    "transporte y a la persistencia.",
                    "Antes de escribir endpoints, definí qué capacidades reales ofrece tu "
                    "producto: suscripciones, facturación, permisos, onboarding. Esos "
                    "límites son los que después justifican módulos y casos de uso.",
                ),
                bullets=(
                    "Modelá capacidades del negocio antes de modelar rutas HTTP.",
                    "Separá comandos de consultas cuando la complejidad lo pida.",
                    "Nombrá módulos según lenguaje del negocio, no del framework.",
                ),
            ),
            ArticleSection(
                title="2. Dominio fuerte, aplicación delgada",
                paragraphs=(
                    "Si toda la lógica vive en handlers gigantes o servicios utilitarios, "
                    "no tenés arquitectura: tenés una bolsa de procedimientos. Las reglas "
                    "importantes tienen que vivir cerca de las entidades y value objects "
                    "que representan el negocio.",
                    "La capa de aplicación debería coordinar dependencias y flujo, pero la "
                    "decisión sobre qué está permitido o prohibido debe vivir en el "
                    "dominio. Ahí está la parte que más cuesta cambiar si la dejás mal.",
                ),
            ),
            ArticleSection(
                title="3. Infraestructura como detalle, no como centro del diseño",
                paragraphs=(
                    "Repositorios, proveedores externos, colas y correo son decisiones de "
                    "implementación. Importan muchísimo, pero no deberían obligarte a "
                    "reescribir la lógica del producto cuando cambian.",
                    "Cuando tratás la infraestructura como detalle, podés evolucionar desde "
                    "una API simple hasta procesos asíncronos, eventos o integraciones sin "
                    "romper la base conceptual del sistema.",
                ),
                bullets=(
                    "Definí puertos claros en aplicación o dominio.",
                    "Mantené DTOs y contratos de infraestructura fuera de las entidades.",
                    "Testeá casos de uso sin levantar la base de datos.",
                ),
            ),
        ),
    ),
    BlogArticle(
        slug="angular-signals-fronteras-ui",
        title="Angular Signals y fronteras de UI: dónde simplifican de verdad",
        summary=(
            "Cuándo usar Signals para volver predecible la UI y cuándo estás moviendo "
            "complejidad de lugar en vez de reducirla."
        ),
        published_at="08 Nov 2025",
        read_time="7 min",
        categories=("Frontend", "Angular"),
        hero_image=(
            "https://images.unsplash.com/photo-1633356122544-f134324a6cee"
            "?w=1200&h=720&fit=crop"
        ),
        eyebrow="Estado reactivo sin humo",
        hero_note="Signals brillan cuando la frontera entre derivación y side effects está clara.",
        intro=(
            "Signals no son magia. Son una herramienta excelente para expresar estado "
            "derivado y relaciones reactivas explícitas, especialmente cuando venís de "
            "componentes llenos de setters, subscriptions y efectos mezclados."
        ),
        takeaways=(
            "Usá signals para derivación explícita y legible.",
            "No mezcles efectos de red con estado de presentación sin una frontera clara.",
            "La simplicidad viene de modelar bien, no del API nuevo por sí solo.",
        ),
        sections=(
            ArticleSection(
                title="1. Qué problema resuelven mejor",
                paragraphs=(
                    "Signals hacen visible qué cambia y por qué cambia. Eso baja mucho la "
                    "carga mental cuando una pantalla tiene filtros, paginación, métricas "
                    "derivadas y estados intermedios de carga.",
                    "La mejora real aparece cuando separás el estado fuente de los valores "
                    "derivados que la UI necesita para renderizar con confianza.",
                ),
            ),
            ArticleSection(
                title="2. Dónde conviene frenar",
                paragraphs=(
                    "Si cada click termina disparando efectos complejos, sincronización con "
                    "backend y múltiples invalidaciones cruzadas, cambiar Observables por "
                    "Signals no corrige el diseño. Solo cambia el lugar donde sufrís.",
                ),
                bullets=(
                    "Separá eventos de usuario de sincronización con backend.",
                    "Centralizá reglas de negocio fuera del template.",
                    "Evitá computed anidados que escondan demasiada lógica.",
                ),
            ),
        ),
    ),
    BlogArticle(
        slug="reflex-product-pages-contenido-estatico",
        title="Reflex para páginas de producto: cuándo el contenido estático alcanza",
        summary=(
            "Una estrategia pragmática para construir páginas ricas en Reflex antes de "
            "meter CMS, base de datos o automatizaciones que todavía no se justifican."
        ),
        published_at="03 Nov 2025",
        read_time="6 min",
        categories=("Backend", "Reflex", "Producto"),
        hero_image=(
            "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5"
            "?w=1200&h=720&fit=crop"
        ),
        eyebrow="Producto antes que integración",
        hero_note="Primero hacé que la experiencia sea clara; después automatizá la fuente.",
        intro=(
            "Hay equipos que conectan una base de datos demasiado pronto y terminan con "
            "una experiencia pobre, solo que ahora es dinámicamente pobre. Para landings, "
            "blogs tempranos o páginas de prueba, el contenido local bien estructurado "
            "suele ser suficiente."
        ),
        takeaways=(
            "Contenido local puede ser una decisión estratégica, no un atajo improvisado.",
            "Si la UX todavía está cambiando, congelar la fuente reduce fricción.",
            "Prepará una forma clara de migrar a CMS cuando el volumen sí lo pida.",
        ),
        sections=(
            ArticleSection(
                title="1. Cuándo conviene quedarse local",
                paragraphs=(
                    "Si todavía estás validando navegación, jerarquía visual y tono del "
                    "contenido, una fuente estática te da control total y elimina muchas "
                    "variables de debugging.",
                ),
            ),
            ArticleSection(
                title="2. Cómo dejar el camino preparado",
                paragraphs=(
                    "El truco está en modelar el contenido como datos reutilizables desde el "
                    "día uno: slug, resumen, metadata, secciones y relaciones. Así migrar a "
                    "un CMS después deja de ser una reescritura total.",
                ),
                bullets=(
                    "Separá datos de componentes desde el inicio.",
                    "Definí campos coherentes con una futura API o CMS.",
                    "Probá la navegación antes de sumar complejidad operativa.",
                ),
            ),
        ),
    ),
    BlogArticle(
        slug="supabase-auth-roles-equipos-pequenos",
        title="Supabase Auth y roles para equipos pequeños: el mínimo serio",
        summary=(
            "Una base segura para autenticación y autorización sin sobrediseñar desde el "
            "primer sprint."
        ),
        published_at="28 Oct 2025",
        read_time="6 min",
        categories=("Backend", "Supabase", "Seguridad"),
        hero_image=(
            "https://images.unsplash.com/photo-1614064641938-3bbee52942c7"
            "?w=1200&h=720&fit=crop"
        ),
        eyebrow="Seguridad pragmática",
        hero_note="No hace falta una plataforma enterprise para dejar de improvisar permisos.",
        intro=(
            "El objetivo no es construir un sistema de permisos infinito. El objetivo es "
            "evitar el caos más común: roles ambiguos, políticas copiadas y validaciones "
            "duplicadas entre frontend y backend."
        ),
        takeaways=(
            "Definí pocos roles y que cada uno tenga intención clara.",
            "RLS protege datos; la aplicación comunica permisos y experiencia.",
            "Documentar reglas ahorra más bugs que sumar excepciones rápidas.",
        ),
        sections=(
            ArticleSection(
                title="1. Menos roles, más claridad",
                paragraphs=(
                    "Arrancar con admin, editor y viewer suele ser suficiente para muchísimos "
                    "productos. Cada rol extra multiplica decisiones y bordes difíciles de "
                    "mantener.",
                ),
            ),
            ArticleSection(
                title="2. Separá autorización de navegación",
                paragraphs=(
                    "La autorización real vive del lado del dato y de las políticas. La UI "
                    "debe acompañar, esconder acciones inválidas y explicar límites, pero no "
                    "simular seguridad que no existe en backend.",
                ),
            ),
        ),
    ),
)


def article_href(slug: str) -> str:
    return f"/blog/{slug}"


def get_article_by_slug(slug: str) -> BlogArticle | None:
    return next((article for article in BLOG_ARTICLES if article.slug == slug), None)


def related_articles(current_slug: str, limit: int = 3) -> tuple[BlogArticle, ...]:
    return tuple(article for article in BLOG_ARTICLES if article.slug != current_slug)[
        :limit
    ]


def categories() -> tuple[str, ...]:
    values = sorted(
        {category for article in BLOG_ARTICLES for category in article.categories}
    )
    return tuple(values)


def articles_by_category(category: str) -> tuple[BlogArticle, ...]:
    return tuple(article for article in BLOG_ARTICLES if category in article.categories)


def category_anchor(category: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", category.lower()).strip("-")
    return normalized or "categoria"
