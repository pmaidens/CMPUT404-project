# push to client
cd client
git init
git add . --all
git commit -m "Push to openshift"
git remote add openshift -f ssh://56da1ff089f5cf181f0000b5@front-c404.rhcloud.com/~/git/front.git/
echo 'merge in openshift'
git merge openshift/master -s recursive -X ours --no-edit
echo 'remove index.html'
rm index.html
echo 'push'
git push openshift HEAD
echo 'remove .git'
rm -rf .git
cd ..

#push to server
cd BloggingAPI
git init
git add . --all
git commit -m "Push to openshift"
git remote add openshift -f ssh://56d513e20c1e66012500005b@project-c404.rhcloud.com/~/git/project.git/
echo 'push'
git push openshift master -f
git clean -fd
echo 'remove .git'
rm -rf .git
cd ..
