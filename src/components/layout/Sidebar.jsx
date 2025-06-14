import React from 'react';
import { 
  FolderGit2, 
  History, 
  Settings, 
  HelpCircle,
  ChevronDown,
  GitBranch,
  Clock,
  CheckCircle2
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useAppContext } from '@/contexts/AppContext';

const Sidebar = () => {
  const { currentRepository, repositories } = useAppContext();

  const mockRepositories = [
    { id: 1, name: 'my-website', status: 'clean', lastUpdate: '2 hours ago' },
    { id: 2, name: 'portfolio-site', status: 'dirty', lastUpdate: '1 day ago' },
    { id: 3, name: 'blog-content', status: 'clean', lastUpdate: '3 days ago' },
  ];

  const currentRepo = currentRepository || mockRepositories[0];

  return (
    <aside className="w-80 border-r bg-sidebar">
      <div className="flex h-full flex-col">
        {/* Repository Selector */}
        <div className="p-6 border-b">
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-sidebar-foreground mb-2 block">
                Current Repository
              </label>
              <Select defaultValue={currentRepo.name}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select repository" />
                </SelectTrigger>
                <SelectContent>
                  {mockRepositories.map((repo) => (
                    <SelectItem key={repo.id} value={repo.name}>
                      <div className="flex items-center space-x-2">
                        <FolderGit2 className="h-4 w-4" />
                        <span>{repo.name}</span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>

        {/* Repository Info */}
        <div className="p-6 border-b">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center space-x-2">
                <FolderGit2 className="h-4 w-4" />
                <span>{currentRepo.name}</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Status</span>
                <Badge variant={currentRepo.status === 'clean' ? 'default' : 'secondary'}>
                  {currentRepo.status === 'clean' ? (
                    <>
                      <CheckCircle2 className="h-3 w-3 mr-1" />
                      Up to date
                    </>
                  ) : (
                    <>
                      <Clock className="h-3 w-3 mr-1" />
                      Changes pending
                    </>
                  )}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Branch</span>
                <div className="flex items-center space-x-1">
                  <GitBranch className="h-3 w-3" />
                  <span className="text-sm">main</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Last update</span>
                <span className="text-sm">{currentRepo.lastUpdate}</span>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Navigation */}
        <div className="flex-1 p-6">
          <nav className="space-y-2">
            <Button variant="ghost" className="w-full justify-start">
              <FolderGit2 className="mr-2 h-4 w-4" />
              Files
            </Button>
            <Button variant="ghost" className="w-full justify-start">
              <History className="mr-2 h-4 w-4" />
              History
            </Button>
            <Button variant="ghost" className="w-full justify-start">
              <Settings className="mr-2 h-4 w-4" />
              Settings
            </Button>
            <Button variant="ghost" className="w-full justify-start">
              <HelpCircle className="mr-2 h-4 w-4" />
              Help
            </Button>
          </nav>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;

