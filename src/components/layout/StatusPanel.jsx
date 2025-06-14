import React from 'react';
import { GitCommit, Clock, User } from 'lucide-react';
import {Button} from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';

const StatusPanel = () => {
  // Mock data for demonstration
  const recentCommits = [
    {
      id: 1,
      message: 'Update homepage content',
      author: 'John Doe',
      time: '2 hours ago',
      hash: 'a1b2c3d'
    },
    {
      id: 2,
      message: 'Fix navigation menu styling',
      author: 'John Doe',
      time: '1 day ago',
      hash: 'e4f5g6h'
    },
    {
      id: 3,
      message: 'Add new blog post',
      author: 'John Doe',
      time: '3 days ago',
      hash: 'i7j8k9l'
    }
  ];

  const pendingChanges = [
    { file: 'index.html', status: 'modified' },
    { file: 'styles.css', status: 'modified' },
    { file: 'new-page.html', status: 'added' }
  ];

  return (
    <div className="w-80 border-l bg-background p-6 space-y-6">
      {/* Repository Status */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base">Repository Status</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Branch</span>
            <Badge variant="outline">main</Badge>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Status</span>
            <Badge variant={pendingChanges.length > 0 ? 'secondary' : 'default'}>
              {pendingChanges.length > 0 ? 'Changes pending' : 'Up to date'}
            </Badge>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Last sync</span>
            <span className="text-sm">2 hours ago</span>
          </div>
        </CardContent>
      </Card>

      {/* Pending Changes */}
      {pendingChanges.length > 0 && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Pending Changes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {pendingChanges.map((change, index) => (
                <div key={index} className="flex items-center justify-between py-2">
                  <span className="text-sm font-medium">{change.file}</span>
                  <Badge 
                    variant={change.status === 'added' ? 'default' : 'secondary'}
                    className="text-xs"
                  >
                    {change.status}
                  </Badge>
                </div>
              ))}
            </div>
            <Separator className="my-4" />
            <Button className="w-full" size="sm">
              <GitCommit className="mr-2 h-4 w-4" />
              Commit Changes
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Recent Activity */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base">Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentCommits.map((commit, index) => (
              <div key={commit.id} className="space-y-2">
                <div className="flex items-start space-x-2">
                  <GitCommit className="h-4 w-4 mt-0.5 text-muted-foreground" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium leading-tight">
                      {commit.message}
                    </p>
                    <div className="flex items-center space-x-2 mt-1">
                      <div className="flex items-center space-x-1">
                        <User className="h-3 w-3 text-muted-foreground" />
                        <span className="text-xs text-muted-foreground">
                          {commit.author}
                        </span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Clock className="h-3 w-3 text-muted-foreground" />
                        <span className="text-xs text-muted-foreground">
                          {commit.time}
                        </span>
                      </div>
                    </div>
                    <Badge variant="outline" className="text-xs mt-1">
                      {commit.hash}
                    </Badge>
                  </div>
                </div>
                {index < recentCommits.length - 1 && (
                  <Separator className="ml-6" />
                )}
              </div>
            ))}
          </div>
          <Separator className="my-4" />
          <Button variant="outline" className="w-full" size="sm">
            View Full History
          </Button>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base">Quick Actions</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <Button variant="outline" className="w-full justify-start" size="sm">
            Sync Repository
          </Button>
          <Button variant="outline" className="w-full justify-start" size="sm">
            View on GitHub
          </Button>
          <Button variant="outline" className="w-full justify-start" size="sm">
            Download Repository
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default StatusPanel;

