import React from 'react';
import { Upload, GitCommit, History, Settings } from 'lucide-react';
import { Button } from '@/components/ui/button';
// import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Card, CardContent, CardHeader, CardTitle} from  '@/components/ui/card';
import FileUploader from '@/components/features/FileUploader';

const Dashboard = () => {
  const handleFilesSelected = (files) => {
    console.log('Files selected:', files);
    // Here you would typically handle the file upload logic
  };

  return (
    <div className="p-6 space-y-6">
      {/* Welcome Section */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Welcome to GitEasy</h1>
        <p className="text-muted-foreground text-lg">
          Manage your GitHub repositories with the simplicity of drag and drop
        </p>
      </div>

      {/* Main Upload Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Upload className="h-5 w-5" />
                <span>Upload Files</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <FileUploader onFilesSelected={handleFilesSelected} />
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button className="w-full justify-start" variant="outline">
                <GitCommit className="mr-2 h-4 w-4" />
                Create Commit
              </Button>
              <Button className="w-full justify-start" variant="outline">
                <History className="mr-2 h-4 w-4" />
                View History
              </Button>
              <Button className="w-full justify-start" variant="outline">
                <Settings className="mr-2 h-4 w-4" />
                Repository Settings
              </Button>
            </CardContent>
          </Card>

          {/* Getting Started */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Getting Started</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="text-sm space-y-2">
                <p className="font-medium">New to Git?</p>
                <p className="text-muted-foreground">
                  GitEasy makes version control simple. Just drag and drop your files, 
                  write a commit message, and we'll handle the rest.
                </p>
                <Button variant="link" className="p-0 h-auto text-sm">
                  Learn more →
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Features Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <Upload className="h-6 w-6 text-primary" />
              </div>
              <div>
                <h3 className="font-semibold">Simple Upload</h3>
                <p className="text-sm text-muted-foreground">
                  Drag and drop files or browse to upload
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <GitCommit className="h-6 w-6 text-primary" />
              </div>
              <div>
                <h3 className="font-semibold">Auto Commit</h3>
                <p className="text-sm text-muted-foreground">
                  Automatic Git operations with smart messages
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <History className="h-6 w-6 text-primary" />
              </div>
              <div>
                <h3 className="font-semibold">Version History</h3>
                <p className="text-sm text-muted-foreground">
                  Track changes and revert when needed
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;

