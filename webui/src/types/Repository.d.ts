export type Repository = {
  id: number;
  full_name: string;
  private: boolean;
  html_url: string;
  description: null | string;
  owner: RepoOwner;
};

export type RepoOwner = {
  id: number;
  login: string;
  avatar_url: string;
};
