import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Link } from "@tanstack/react-router";
import { Breadcrumbs } from "../common/Breadcrumbs";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { useUser } from "@/hooks/auth";
import { Input } from "../ui/input";
import { Search } from "lucide-react";

export function Navbar() {
  const { user } = useUser();

  const breadcrumbs = [{ display: "Dashboard", href: "/dashboard" }];

  return (
    <div className="flex justify-between items-center w-full p-4 border-b bg-background/90">
      <div className="flex items-center gap-4">
        <Link to="/" className="font-semibold text-lg">
          {/* TODO: add logo */}
          eVault
        </Link>
        <Breadcrumbs paths={breadcrumbs} />
      </div>
      <div className="flex items-center align-middle gap-2">
        {/* TODO: add search functionality */}
        <div className="relative">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2" />
          <Input
            type="text"
            placeholder="Search"
            className="peer block w-full rounded-md border py-[9px] pl-10 text-sm"
          />
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger className="cursor-pointer">
            <Avatar>
              <AvatarImage src={user?.avatar_url} />
              <AvatarFallback>{user?.name?.charAt(0)}</AvatarFallback>
            </Avatar>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuLabel>
              {user && (
                <div className="flex flex-col">
                  <p className="font-medium text-lg">{user.name}</p>
                  <p className="text-sm text-muted-foreground">{user.login}</p>
                </div>
              )}
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem>Settings</DropdownMenuItem>
            <DropdownMenuItem>Sign out</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  );
}
