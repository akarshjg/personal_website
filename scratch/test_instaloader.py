import instaloader

def main():
    L = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(L.context, "aio.wiz")
        print(f"Profile: {profile.username}")
        print(f"Followers: {profile.followers}")
        print(f"Posts: {profile.mediacount}")
        
        posts = []
        for post in profile.get_posts():
            print(f"Post URL: {post.url}")
            print(f"Caption: {post.caption}")
            posts.append(post)
            if len(posts) >= 5:
                break
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
