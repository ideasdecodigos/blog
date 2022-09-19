-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 14, 2022 at 12:35 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `idcschools`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `likes` (IN `id_post` INT, IN `id_user` INT)   BEGIN
DECLARE LIKES INT;
SELECT COUNT(*) INTO LIKES FROM posts_likes WHERE post_like = id_post AND user_like = id_user;
IF (LIKES >= 1) THEN
	DELETE FROM posts_likes WHERE post_like=id_post AND user_like=id_user;
 ELSE
   INSERT INTO posts_likes VALUES(id_post, id_user);
 END IF;
 END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `set_posts_views` (IN `id_post` INT)   BEGIN
DECLARE VIEWCNT INT;
SELECT SUM(counter_view) INTO VIEWCNT FROM posts_views WHERE post_view=id_post;

IF (VIEWCNT >= 0)THEN
UPDATE posts_views SET counter_view=(VIEWCNT + 1) WHERE post_view=id_post;
ELSE
INSERT INTO posts_views VALUES(id_post, 1);
END IF;

END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `switch_favorite_comment` (IN `id_comment` INT, IN `id_user` INT)   BEGIN
DECLARE FAVORITE INT;
SELECT COUNT(*) INTO FAVORITE FROM comments_likes WHERE comment_favorite = id_comment AND user_favorite = id_user;
IF (FAVORITE >= 1) THEN
	DELETE FROM comments_likes WHERE comment_favorite=id_comment AND user_favorite=id_user;
 ELSE
   INSERT INTO comments_likes VALUES(id_comment, id_user);
 END IF;
 END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE `comments` (
  `id_comment` int(11) NOT NULL,
  `post_comment` int(11) NOT NULL,
  `user_comment` int(11) NOT NULL,
  `content_comment` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_reply` int(11) NOT NULL,
  `content_reply` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_comment` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `comments`
--

INSERT INTO `comments` (`id_comment`, `post_comment`, `user_comment`, `content_comment`, `id_reply`, `content_reply`, `date_comment`) VALUES
(34, 26, 10, '<p>hofaslj fasdjlkfasso fajskdfj aosd fasdofjao sdf asjdfo asdjf odsaj foas dfo a</p>', 0, '', '2022-09-07 01:01:38'),
(35, 26, 10, '<p>pata que?</p>', 34, '#hofaslj fasdjlkfasso fajskdfj aosd fasdofjao sdf asjdfo asdjf odsaj foas dfo a', '2022-09-07 01:05:51'),
(37, 26, 10, '<p>&#128526;</p>', 0, '', '2022-09-07 01:06:29'),
(38, 26, 10, '<p>oh my god</p>', 37, '#&#128526;', '2022-09-07 16:25:11'),
(40, 28, 10, '<p>fasdf</p>', 0, '', '2022-09-13 01:42:37'),
(41, 28, 10, '<p>fasdg</p>', 0, '', '2022-09-13 01:42:41'),
(42, 29, 10, '<p>fasssss</p>', 0, '', '2022-09-13 01:42:56'),
(43, 28, 10, '<p>fasdfa</p>', 0, '', '2022-09-13 01:54:04'),
(44, 28, 10, '<p>fasdfas</p>', 0, '', '2022-09-13 01:54:06'),
(45, 28, 10, '<p>fasdfas</p>', 0, '', '2022-09-13 01:54:09');

--
-- Triggers `comments`
--
DELIMITER $$
CREATE TRIGGER `comments_after_insert` AFTER INSERT ON `comments` FOR EACH ROW BEGIN 
    DECLARE NAME VARCHAR(50);
    DECLARE TITLE TEXT;
    SELECT name_user INTO NAME FROM users WHERE id_user=new.user_comment;
    SELECT title_post INTO TITLE FROM posts WHERE id_post=new.post_comment;
    
    INSERT INTO notifications(post_info, user_info,target_info, content_info, scope_info, table_info)
    	VALUES(new.post_comment, new.user_comment, new.id_comment, CONCAT(NAME, " has commented your post, titled: ", TITLE), "private", "comments");
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `comments_likes`
--

CREATE TABLE `comments_likes` (
  `comment_favorite` int(11) NOT NULL,
  `user_favorite` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `comments_likes`
--

INSERT INTO `comments_likes` (`comment_favorite`, `user_favorite`) VALUES
(35, 10),
(37, 10);

--
-- Triggers `comments_likes`
--
DELIMITER $$
CREATE TRIGGER `comments_likes_after_insert` AFTER INSERT ON `comments_likes` FOR EACH ROW BEGIN 
    DECLARE NAME VARCHAR(50);
    DECLARE TITLE TEXT;
    DECLARE IDPOST INT;
    
    SELECT name_user INTO NAME FROM users WHERE id_user=new.user_favorite;    
    SELECT id_post INTO IDPOST FROM posts INNER JOIN comments 
    ON posts.id_post=comments.post_comment INNER JOIN comments_likes 
    ON comments.id_comment=comments_likes.comment_favorite 
    WHERE comment_favorite=new.comment_favorite;
    
    SELECT title_post INTO TITLE FROM posts INNER JOIN comments 
    ON posts.id_post=comments.post_comment INNER JOIN comments_likes 
    ON comments.id_comment=comments_likes.comment_favorite 
    WHERE comment_favorite=new.comment_favorite;
    
    INSERT INTO notifications(post_info, user_info, target_info, content_info, scope_info, table_info)
    	VALUES(IDPOST, new.user_favorite, new.comment_favorite, CONCAT(NAME, " liked your post's comment, titled: ", TITLE), "private", "comments_likes");
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `followers`
--

CREATE TABLE `followers` (
  `followed` int(11) NOT NULL,
  `follower` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Triggers `followers`
--
DELIMITER $$
CREATE TRIGGER `followers_after_insert` AFTER INSERT ON `followers` FOR EACH ROW BEGIN 
    DECLARE FOLLOWER VARCHAR(50);    
    SELECT name_user INTO FOLLOWER FROM users WHERE id_user=new.follower;
    
    INSERT INTO notifications(user_info,target_info, content_info, scope_info, table_info)
    	VALUES(new.followed, new.follower, CONCAT(FOLLOWER, " started to follow you. follow back..."), "private", "followers");
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id_info` int(11) NOT NULL,
  `post_info` int(11) NOT NULL,
  `user_info` int(11) NOT NULL,
  `target_info` int(11) NOT NULL,
  `content_info` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `scope_info` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `table_info` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status_info` varchar(5) CHARACTER SET utf8mb4 NOT NULL DEFAULT 'true',
  `date_info` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id_info`, `post_info`, `user_info`, `target_info`, `content_info`, `scope_info`, `table_info`, `status_info`, `date_info`) VALUES
(89, 0, 10, 0, 'Welcome jonh smith scar\n Thank you for start joining our community!', 'private', 'users', 'true', '2022-09-06 10:47:36'),
(90, 0, 11, 0, 'Welcome maria\n Thank you for start joining our community!', 'private', 'users', 'true', '2022-09-06 10:48:08'),
(91, 26, 11, 0, 'Have a look to maria\'s post, titled: un tema de aves', 'public', 'posts', 'true', '2022-09-06 10:48:57'),
(92, 27, 10, 0, 'Have a look to jonh smith scar\'s post, titled: un vacan &#128522;', 'public', 'posts', 'true', '2022-09-06 10:49:47'),
(93, 26, 10, 34, 'jonh smith scar has commented your post, titled: un tema de aves', 'private', 'comments', 'true', '2022-09-07 01:01:38'),
(94, 26, 10, 34, 'jonh smith scar liked your post\'s comment, titled: un tema de aves', 'private', 'comments_likes', 'true', '2022-09-07 01:04:00'),
(95, 26, 10, 35, 'jonh smith scar has commented your post, titled: un tema de aves', 'private', 'comments', 'true', '2022-09-07 01:05:51'),
(96, 26, 10, 36, 'jonh smith scar has commented your post, titled: un tema de aves', 'private', 'comments', 'true', '2022-09-07 01:06:08'),
(97, 26, 10, 37, 'jonh smith scar has commented your post, titled: un tema de aves', 'private', 'comments', 'true', '2022-09-07 01:06:29'),
(98, 26, 10, 37, 'jonh smith scar liked your post\'s comment, titled: un tema de aves', 'private', 'comments_likes', 'true', '2022-09-07 02:17:47'),
(99, 26, 10, 37, 'jonh smith scar liked your post\'s comment, titled: un tema de aves', 'private', 'comments_likes', 'true', '2022-09-07 02:17:50'),
(100, 26, 10, 37, 'jonh smith scar liked your post\'s comment, titled: un tema de aves', 'private', 'comments_likes', 'true', '2022-09-07 02:17:52'),
(101, 26, 10, 38, 'jonh smith scar has commented your post, titled: un tema de aves', 'private', 'comments', 'true', '2022-09-07 16:25:11'),
(102, 26, 10, 35, 'jonh smith scar liked your post\'s comment, titled: un tema de aves', 'private', 'comments_likes', 'true', '2022-09-07 20:55:50'),
(103, 26, 10, 0, 'jonh smith scar liked your post, titled: un tema de aves', 'private', 'posts_likes', 'true', '2022-09-07 21:12:31'),
(104, 27, 10, 39, 'jonh smith scar has commented your post, titled: un vacan &#128522;', 'private', 'comments', 'true', '2022-09-11 20:10:18'),
(105, 28, 10, 0, 'Have a look to jonh smith scar\'s post, titled: todo el mundo mea', 'public', 'posts', 'true', '2022-09-11 20:16:42'),
(106, 28, 10, 0, 'jonh smith scar liked your post, titled: todo el mundo mea', 'private', 'posts_likes', 'true', '2022-09-11 20:37:30'),
(107, 29, 10, 0, 'Have a look to jonh smith scar\'s post, titled: el hotpital mas grande', 'public', 'posts', 'true', '2022-09-11 22:51:26'),
(108, 29, 10, 0, 'jonh smith scar liked your post, titled: el hotpital mas grande', 'private', 'posts_likes', 'true', '2022-09-12 02:26:03'),
(109, 29, 10, 0, 'jonh smith scar liked your post, titled: el hotpital mas grande', 'private', 'posts_likes', 'true', '2022-09-12 02:26:10'),
(110, 28, 10, 40, 'jonh smith scar has commented your post, titled: todo el mundo mea', 'private', 'comments', 'true', '2022-09-13 01:42:37'),
(111, 28, 10, 41, 'jonh smith scar has commented your post, titled: todo el mundo mea', 'private', 'comments', 'true', '2022-09-13 01:42:41'),
(112, 29, 10, 42, 'jonh smith scar has commented your post, titled: el hotpital mas grande', 'private', 'comments', 'true', '2022-09-13 01:42:56'),
(113, 28, 10, 43, 'jonh smith scar has commented your post, titled: todo el mundo mea', 'private', 'comments', 'true', '2022-09-13 01:54:04'),
(114, 28, 10, 44, 'jonh smith scar has commented your post, titled: todo el mundo mea', 'private', 'comments', 'true', '2022-09-13 01:54:06'),
(115, 28, 10, 45, 'jonh smith scar has commented your post, titled: todo el mundo mea', 'private', 'comments', 'true', '2022-09-13 01:54:09'),
(116, 28, 10, 40, 'jonh smith scar liked your post\'s comment, titled: todo el mundo mea', 'private', 'comments_likes', 'true', '2022-09-13 02:16:40'),
(117, 26, 10, 37, 'jonh smith scar liked your post\'s comment, titled: un tema de aves', 'private', 'comments_likes', 'true', '2022-09-13 18:43:31'),
(118, 30, 10, 0, 'Have a look to jonh smith scar\'s post, titled: The example above does not use the index and array parameters. It can be rewritten to:', 'public', 'posts', 'true', '2022-09-13 19:58:49'),
(119, 28, 10, 0, 'jonh smith scar liked your post, titled: todo el mundo mea', 'private', 'posts_likes', 'true', '2022-09-14 09:57:42');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `id_post` int(11) NOT NULL,
  `title_post` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_post` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `author_post` int(11) NOT NULL,
  `categories_post` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_post` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`id_post`, `title_post`, `content_post`, `author_post`, `categories_post`, `date_post`) VALUES
(26, 'un tema de aves', '<p>totas la aves vuelan &#129392;</p>', 11, 'aves vuelo', '2022-09-06 10:48:57'),
(28, 'todo el mundo mea', '<p>la vida es una</p>\r\n<p>&nbsp;</p>\r\n<p>una&nbsp; fal fasll; fasdfasdl kjfasj fa sdf asdlkf askd f</p>\r\n<p>&nbsp;</p>\r\n<p>fasdlfasjl fsdl oorel lorem*50</p>\r\n<p>fasl;kjfas f asdfklas</p>', 10, 'intorod jquery find child', '2022-09-11 20:16:42'),
(29, 'el hotpital mas grande', '<p>dfa skf a;sdkj fasdfkasd ffasl dfjk asdj fak jsdfjk adskj fjk asdjf asdkjdfjlkaskdjf ;af jksdj fk; asdfk a;sldf kas dfkajs;ldkfj kasjd;flkjasdkjfioqpjeknkzhioafelf k;iadsjfa fdij asdifjoa jsjdip issadjf iasdkfh asdoi f as dhffaksd fliu</p>', 10, 'fajskjlfa fajls dfja d fasjdl fasj dfaj sdfj asd fasd fj asd fasj dkfakj sdfj asddkj fasjk dfjk asdf jasj dfakj sdfk askj dlfaklsj d', '2022-09-11 22:51:26'),
(30, 'The example above does not use the index and array parameters. It can be rewritten to:', '<p>Note that the function takes 4 arguments:</p>\r\n<ul>\r\n<li>The total (the initial value / previously returned value)</li>\r\n<li>The item value</li>\r\n<li>The item index</li>\r\n<li>The array itself</li>\r\n</ul>\r\n<p>The example above does not use the index and array parameters. It can be rewritten to:</p>', 10, 'bivi', '2022-09-13 19:58:49');

--
-- Triggers `posts`
--
DELIMITER $$
CREATE TRIGGER `posts_after_insert` AFTER INSERT ON `posts` FOR EACH ROW BEGIN
DECLARE NAME VARCHAR(50);
SELECT name_user INTO NAME FROM users WHERE id_user=new.author_post;

INSERT INTO notifications(post_info, user_info, content_info, scope_info, table_info)
VALUES(new.id_post, new.author_post, CONCAT("Have a look to ", NAME, "'s post, titled: ", new.title_post), "public", "posts");

END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `posts_likes`
--

CREATE TABLE `posts_likes` (
  `post_like` int(11) NOT NULL,
  `user_like` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `posts_likes`
--

INSERT INTO `posts_likes` (`post_like`, `user_like`) VALUES
(26, 10),
(28, 10);

--
-- Triggers `posts_likes`
--
DELIMITER $$
CREATE TRIGGER `post_likes_after_insert` AFTER INSERT ON `posts_likes` FOR EACH ROW BEGIN 
    DECLARE NAME VARCHAR(50);
    DECLARE TITLE TEXT;
    SELECT name_user INTO NAME FROM users WHERE id_user=new.user_like;
    SELECT title_post INTO TITLE FROM posts WHERE id_post=new.post_like;
    
    INSERT INTO notifications(post_info, user_info, content_info, scope_info, table_info)
    	VALUES(new.post_like, new.user_like, CONCAT(NAME, " liked your post, titled: ", TITLE), "private", "posts_likes");
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `posts_views`
--

CREATE TABLE `posts_views` (
  `post_view` int(11) NOT NULL,
  `counter_view` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `posts_views`
--

INSERT INTO `posts_views` (`post_view`, `counter_view`) VALUES
(26, 224),
(28, 96),
(29, 121);

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `id_report` int(11) NOT NULL,
  `user_report` int(11) NOT NULL,
  `origen_report` int(11) NOT NULL,
  `action_report` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `info_report` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `table_report` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_report` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id_user` int(11) NOT NULL,
  `name_user` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mail_user` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pass_user` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_user` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `country_user` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `about_user` text CHARACTER SET utf8 NOT NULL DEFAULT 'Hi, welcome to my profile',
  `foto_user` longtext CHARACTER SET utf8 NOT NULL,
  `wallpaper_user` longtext CHARACTER SET utf8 NOT NULL,
  `date_user` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id_user`, `name_user`, `mail_user`, `pass_user`, `phone_user`, `country_user`, `about_user`, `foto_user`, `wallpaper_user`, `date_user`) VALUES
(10, 'jonh smith scar', 'jonh@gmail.com', 'pbkdf2:sha256:260000$HOfmUtvVBRRSVkM2$9f172cf39018fd1ea93fae7d7c8a6b02a28a9dd519d04c3aaa615e73a1a80e87', '', '', 'Hi, welcome to my profile', '../static/uploads/20200611_055242.jpg', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTIhdi1VeIiPbfqAIU6HOWCcMZqMLPbtcAslQ&usqp=CAU', '2022-09-06 10:47:36'),
(11, 'maria', 'maria@gmail.com', 'pbkdf2:sha256:260000$t6PuJ0pQ4Efd3xW9$dbb29a914c68f4f4f3d469da9d9b1ad160e90aee2963a45a249d87e362cb5ccc', '', '', 'Hi, welcome to my profile', '', '', '2022-09-06 10:48:08');

--
-- Triggers `users`
--
DELIMITER $$
CREATE TRIGGER `users_after_insert` AFTER INSERT ON `users` FOR EACH ROW BEGIN
	INSERT INTO notifications(user_info, content_info, scope_info, table_info) 
    VALUES(new.id_user,CONCAT('Welcome ', new.name_user, '\n Thank you for start joining our community!'), "private", "users");

END
$$
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id_comment`),
  ADD KEY `user_comment` (`user_comment`),
  ADD KEY `post_comment` (`post_comment`);

--
-- Indexes for table `comments_likes`
--
ALTER TABLE `comments_likes`
  ADD KEY `comment_favorite` (`comment_favorite`),
  ADD KEY `user_favorite` (`user_favorite`);

--
-- Indexes for table `followers`
--
ALTER TABLE `followers`
  ADD KEY `followed` (`followed`),
  ADD KEY `follower` (`follower`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id_info`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`id_post`),
  ADD KEY `author_post` (`author_post`);

--
-- Indexes for table `posts_likes`
--
ALTER TABLE `posts_likes`
  ADD KEY `post_like` (`post_like`),
  ADD KEY `user_like` (`user_like`);

--
-- Indexes for table `posts_views`
--
ALTER TABLE `posts_views`
  ADD KEY `post_view` (`post_view`);

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`id_report`),
  ADD KEY `user_report` (`user_report`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `comments`
--
ALTER TABLE `comments`
  MODIFY `id_comment` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id_info` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=120;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `id_post` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `reports`
--
ALTER TABLE `reports`
  MODIFY `id_report` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`user_comment`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`post_comment`) REFERENCES `posts` (`id_post`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `comments_likes`
--
ALTER TABLE `comments_likes`
  ADD CONSTRAINT `comments_likes_ibfk_1` FOREIGN KEY (`comment_favorite`) REFERENCES `comments` (`id_comment`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `comments_likes_ibfk_2` FOREIGN KEY (`user_favorite`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `followers`
--
ALTER TABLE `followers`
  ADD CONSTRAINT `followers_ibfk_1` FOREIGN KEY (`followed`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `followers_ibfk_2` FOREIGN KEY (`follower`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`author_post`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `posts_likes`
--
ALTER TABLE `posts_likes`
  ADD CONSTRAINT `posts_likes_ibfk_1` FOREIGN KEY (`post_like`) REFERENCES `posts` (`id_post`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `posts_likes_ibfk_2` FOREIGN KEY (`user_like`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `posts_views`
--
ALTER TABLE `posts_views`
  ADD CONSTRAINT `posts_views_ibfk_1` FOREIGN KEY (`post_view`) REFERENCES `posts` (`id_post`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `reports`
--
ALTER TABLE `reports`
  ADD CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`user_report`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
