from website_frontend.integrations.supabase import SupabaseAPI
from website_frontend.model.featured import Featured


SUPABASE_API = SupabaseAPI()


def get_featured_projects() -> list[Featured]:
    return SUPABASE_API.featured()
